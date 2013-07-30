import collections
import itertools

from django import forms

from explodio.common import iterator
from explodio.common.forms import FormHelpersMixin
from explodio.xfit import models


WODExerciseForm_CLONE_FIELDS = ('effort', 'reps', 'notes')

class TimeForm(forms.Form):
    time = forms.TimeField()

class RoundsForm(forms.Form):
    rounds = forms.IntegerField(min_value=0)

class WODExerciseForm(forms.ModelForm, FormHelpersMixin):

    REQUIRE_IF_CLONE = (
        ('effort', 'effort_unit'),
        ('reps', 'reps_unit'),
    )

    class Meta:
        fields = WODExerciseForm_CLONE_FIELDS
        model = models.WODExercise

    def __init__(self, goal, *args, **kwargs):
        super(WODExerciseForm, self).__init__(*args, **kwargs)

        self.goal = goal

        for field in WODExerciseForm_CLONE_FIELDS:
            #self.set_default(field, getattr(goal, field))
            self.set_default(field, '')

        for required, if_clone in WODExerciseForm.REQUIRE_IF_CLONE:
            if not getattr(goal, if_clone):
                del self.fields[required]

    def save(self, user_wod, commit=True):
        instance = super(WODExerciseForm, self).save(commit=False)
        instance.user_wod = user_wod
        instance.goal = self.goal
        if commit:
            instance.save()
        return instance

class UserWODForm(object):

    def __init__(self, user, wod, user_wod, prefix, data):
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
        if self.workout_type == models.Workout.WORKOUT_TYPE_TIMED:
            return TimeForm(self.data)
        elif self.workout_type == models.Workout.WORKOUT_TYPE_AMRAP:
            return RoundsForm(self.data)
        else:
            raise Exception('Unknown workout type')

    def create_wod_exercise_forms(self):
        pairs = self.create_goal_wodexercise_pairs_iter()
        repeated_pairs = self.create_repeated_pairs(pairs)

        wod_exercise_forms = []

        for index, pair in enumerate(repeated_pairs):
            goal, wod_exercise = pair
            prefix = '%s-wode-%s' % (self.prefix, index)
            wod_exercise_form = WODExerciseForm(goal, self.data,
                instance=wod_exercise, prefix=prefix)
            wod_exercise_forms.append(wod_exercise_form)

        return wod_exercise_forms

    def create_goal_wodexercise_pairs_iter(self):
        if not self.user_wod:
            goals = self.wod.workout.exercises.order_by('item_group', 'order')
            wod_exercises = [None] * len(goals)
            pairs = itertools.izip(goals, wod_exercises)
        else:
            goals = self.wod.workout.exercises.order_by('item_group', 'order')
            wod_exercises = self.user_wod.exercises.all()
            pairs = iterator.left_outer_join(goals, wod_exercises,
                searcher=lambda goal, wod_exercise: \
                    wod_exercise.goal.id == goal.id)
            pairs = iter(pairs)
        return pairs

    def create_repeated_pairs(self, goal_wodexercise_pairs):
        group_items = collections.OrderedDict()

        for goal, wod_exercise in goal_wodexercise_pairs:
            group = goal.item_group
            if group not in group_items:
                group_items[group] = []
            group_items[group].append((goal, wod_exercise))

        for group, pairs in group_items.iteritems():
            goal, wod_exercise = pairs[0]
            repeat = goal.item_group_repeats
            for x in xrange(repeat):
                for pair in pairs:
                    yield pair

    def is_valid(self):
        valid = self.score_form and self.score_form.is_valid()
        for wod_exercise_form in self.wod_exercise_forms:
            valid &= wod_exercise_form.is_valid()
        return valid

    def save(self, commit=True):
        if self.user_wod is None:
            user_wod = models.UserWOD(user=self.user, wod=self.wod)
        else:
            user_wod = self.user_wod

        if self.workout_type == models.Workout.WORKOUT_TYPE_TIMED:
            user_wod.time = self.score_form.cleaned_data['time']
            user_wod.rounds = None
        elif self.workout_type == models.Workout.WORKOUT_TYPE_AMRAP:
            user_wod.time = None
            user_wod.rounds = self.score_form.cleaned_data['rounds']

        for wod_exercise_form in self.wod_exercise_forms:
            wod_exercise_form.save(user_wod, commit=commit)

        if commit:
            user_wod.save()

        return user_wod
