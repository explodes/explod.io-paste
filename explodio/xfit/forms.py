import collections
import itertools

from django import forms

from explodio.common import iterator
from explodio.common.forms import FormHelpersMixin
from explodio.xfit import models


class ScoreForm(forms.Form):
    """
    Base form for keeping score of a Workout
    """
    pass

class TimeForm(ScoreForm):
    """
    Score Form for Time
    """
    time = forms.TimeField(required=False, label="Time (HH:MM:SS)")

class RoundsForm(ScoreForm):
    """
    Score Form for Rounds
    """
    rounds = forms.IntegerField(min_value=0, required=False)

class WODExerciseForm(forms.ModelForm, FormHelpersMixin):
    """
    Individual form for a WODExercise for a user to fill out
    """

    # Require fields if the value of the attribute is not empty
    REQUIRE_IF_VALUE = (
        ('effort', 'effort_unit'),
        ('reps', 'reps_unit'),
    )

    class Meta:
        fields = ('effort', 'reps', 'notes')
        model = models.WODExercise

    def __init__(self, goal, *args, **kwargs):
        """
        Construct a WODExerciseForm for a given goal

        effort / reps fields are deleted if they are not set in the goal.

        :param goal: The WorkoutExercise with the target effort/reps
        :param args: ModelForm *args
        :param kwargs: ModelForm **kwargs
        :return: self
        """
        super(WODExerciseForm, self).__init__(*args, **kwargs)

        self.goal = goal

        for required, if_clone in WODExerciseForm.REQUIRE_IF_VALUE:
            if not getattr(goal, if_clone):
                del self.fields[required]

    def save(self, user_wod, commit=True):
        """
        Save this WODExercise to a user_wod
        :param user_wod: The parent UserWOD to save to
        :param commit: Whether or not the commit the save
        :return: The new or updated WODExercise
        """
        instance = super(WODExerciseForm, self).save(commit=False)
        instance.user_wod = user_wod
        instance.goal = self.goal
        if commit:
            instance.save()
        return instance

class UserWODForm(object):

    def __init__(self, user, wod, user_wod, prefix, data):
        """
        Contruct a UserWOD form-container object, of sort which is capable
        of validation and saving

        :param user: User owning the UserWOD
        :param wod: WorkoutOfTheDay this User is performing
        :param user_wod: A pre-existing UserWOD (can be None)
        :param prefix: Form prefix, prevents POST data name collisions
        :param data: Default form data for child forms
        :return: self
        """
        self.data = data
        self.user = user
        self.wod = wod
        self.user_wod = user_wod

        # Calculated
        self.prefix = 'wod-%s-%s' % (wod.id, prefix)
        self.workout_type = self.wod.workout.workout_type

        # Computed
        self.score_form = self.create_score_form()
        self.wod_exercise_forms = self.create_wod_exercise_forms()

    def create_score_form(self):
        """
        Construct the appropriate score form for
        the WorkoutOfTheDay's workout_type
        :return: A django Form
        """
        if self.workout_type == models.Workout.WORKOUT_TYPE_TIMED:
            if self.user_wod:
                initial = {'time': self.user_wod.time}
            else:
                initial = None
            return TimeForm(self.data, prefix=self.prefix, initial=initial)
        elif self.workout_type == models.Workout.WORKOUT_TYPE_AMRAP:
            if self.user_wod:
                initial = {'rounds': self.user_wod.rounds}
            else:
                initial = None
            return RoundsForm(self.data, prefix=self.prefix, initial=initial)
        elif self.workout_type == models.Workout.WORKOUT_TYPE_POWER:
            pass
        else:
            raise Exception('Unknown workout type')

    def create_wod_exercise_forms(self):
        """
        Create children WODExerciseForms, one for each repetition of each
        exercise in the WorkoutOfTheDay's Workout
        :return: list of WODExerciseForms
        """
        pairs = self.create_goal_wodexercise_pairs_iter()

        wod_exercise_forms = []

        for index, pair in enumerate(pairs):
            goal, wod_exercise = pair
            prefix = '%sex%s' % (self.prefix, index)
            wod_exercise_form = WODExerciseForm(goal, self.data,
                instance=wod_exercise, prefix=prefix)
            wod_exercise_forms.append(wod_exercise_form)

        return wod_exercise_forms

    def create_goal_wodexercise_pairs_iter(self):
        """
        Pair the WorkoutOfTheDay's WorkoutExercise the the
        current UserWOD's WODExercises by goal (WorkoutExercise)
        If there is no current user_wod, pairs WorkoutExercises with None.
        :return: list of (WorkoutExercise, WODExercise)
            or (WorkoutExercise, None)
        """
        goals = self.get_repeated_exercises(self.wod.workout)

        if not self.user_wod:
            # If there is no UserWOD, build (WorkoutExercise, None) tuples
            wod_exercises = [None] * len(goals)
            pairs = itertools.izip(goals, wod_exercises)
        else:
            # If there is a UserWOD, build (WorkoutExercise, WODExercise) tuples
            wod_exercises = self.user_wod.wod_exercises \
                .order_by('goal__item_group', 'goal__order', 'pk')
            pairs = iterator.pair_left(goals, wod_exercises, match_once=True,
                searcher=lambda goal, wod_exercise: \
                    wod_exercise.goal.id == goal.id)
            pairs = iter(pairs)
        return pairs

    def get_repeated_exercises(self, workout):
        """
        For each WorkoutExercise group in a Workout, yield that group repeated
        as necessary.

        For example, if the WorkoutExercise set looks like:
        - Exercise 1: Group A repeat 2x
        - Exercise 2: Group A repeat 2x
        - Exercise 3: Group B repeat 1x
        - Exercise 4: Group C repeat 2x
        - Exercise 5: Group C repeat 2x

        The resulting list is:
        > A1, A2, A1,A 2, B3, C4, C5, C4, C5
        :return: list of WorkoutExercise
        """
        exercises = workout.exercises.order_by('item_group', 'order')
        return list(self.repeat_exercises_iter(exercises))

    def repeat_exercises_iter(self, exercises):
        """
        Repeat exercises by `item_group,` `item_group_repeats` times
        :param goals: list of WorkoutExercise
        :return: longer list of WorkoutExercise
        """
        group_items = collections.OrderedDict()

        # In order, add exercises to their respective group
        for exercise in exercises:
            group = exercise.item_group
            if group not in group_items:
                group_items[group] = []
            group_items[group].append(exercise)

        # For each group, yield the items in the groups `n` times
        for group, exercises in group_items.iteritems():
            exercise = exercises[0] # Use the first exercise as
            repeat = exercise.item_group_repeats
            for x in xrange(repeat):
                for exercise in exercises:
                    yield exercise

    def is_valid(self):
        """
        Validate each of the child forms this object has
        :return: Whether or not every child form validated
        """
        valid = not self.score_form or self.score_form.is_valid()
        for wod_exercise_form in self.wod_exercise_forms:
            valid &= wod_exercise_form.is_valid()
        return valid

    def save(self, commit=True):
        """
        Create or update a UserWOD with WODExercises
        :param commit: Whether or not to commit the UserWOD to the database
        :return: The new or updated UserWOD
        """

        # Create a new UserWOD if we need to, or use the initial one
        if self.user_wod is None:
            user_wod = models.UserWOD(user=self.user, wod=self.wod)
        else:
            user_wod = self.user_wod

        # Save time OR rounds
        if self.workout_type == models.Workout.WORKOUT_TYPE_TIMED:
            user_wod.time = self.score_form.cleaned_data['time']
            user_wod.rounds = None
        elif self.workout_type == models.Workout.WORKOUT_TYPE_AMRAP:
            user_wod.time = None
            user_wod.rounds = self.score_form.cleaned_data['rounds']
        elif self.workout_type == models.Workout.WORKOUT_TYPE_POWER:
            user_wod.time = None
            user_wod.rounds = None
        else:
            raise Exception('Unknown workout type')

        # Create a list of WODExercises to save (or not)
        wod_exercises = []
        for wod_exercise_form in self.wod_exercise_forms:
            wod_exercise = wod_exercise_form.save(user_wod, commit=False)
            wod_exercises.append(wod_exercise)

        # If we need to commit, save the UserWOD 1st, then the related objects
        if commit:
            user_wod.save()
            for wod_exercise in wod_exercises:
                wod_exercise.user_wod = user_wod
                wod_exercise.save()

        return user_wod
