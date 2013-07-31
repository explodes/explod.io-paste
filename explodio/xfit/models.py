from django.conf import settings
from django.db import models

from explodio.xfit import managers


class Unit(models.Model):

    title = models.CharField(max_length=50)
    plural = models.CharField(max_length=50)

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'unit'
        verbose_name_plural = 'units'
        ordering = ('title',)

    def __unicode__(self):
        return self.title

class Gym(models.Model):

    title = models.CharField(max_length=50, help_text='Title of this gym')
    slug = models.SlugField(max_length=50, unique=True,
        help_text='Used for URLs')
    active = models.BooleanField(default=True, help_text='Uncheck to disable '
        'this gym on the website')

    order = models.PositiveSmallIntegerField(default=0,
        help_text='Order of appearance')

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.GymManager()

    class Meta:
        verbose_name = 'gym'
        verbose_name_plural = 'gyms'
        ordering = ('order',)

    def __unicode__(self):
        return self.title

class Workout(models.Model):

    WORKOUT_TYPE_AMRAP = 1
    WORKOUT_TYPE_TIMED = 2
    WORKOUT_TYPE_POWER = 3

    WORKOUT_TYPES = (
        (WORKOUT_TYPE_AMRAP, 'AMRAP'),
        (WORKOUT_TYPE_TIMED, 'Timed'),
        (WORKOUT_TYPE_POWER, 'Power'),
    )

    title = models.CharField(max_length=50, help_text='Title of this workout')
    slug = models.SlugField(max_length=50, unique=True, 
        help_text='Used for URLs')
    is_hero = models.BooleanField(default=False, 
        help_text='Whether or not this is a special Hero Workout')

    workout_type = models.PositiveSmallIntegerField(choices=WORKOUT_TYPES,
        default=WORKOUT_TYPE_TIMED,
        help_text='What kind of goal does this workout have?')
    time_limit = models.TimeField(blank=True, null=True,
        help_text='For AMRAP, how much time is allowed')

    notes= models.CharField(max_length=50, blank=True,
        help_text='Optional special instructions')

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.WorkoutManager()

    class Meta:
        verbose_name = 'workout'
        verbose_name_plural = 'workouts'
        ordering = ('title',)

    def __unicode__(self):
        return self.title

class Exercise(models.Model):

    title = models.CharField(max_length=50, help_text='Title of this workout')
    slug = models.SlugField(max_length=50, unique=True,
        help_text='Used for URLs')
    notes = models.CharField(max_length=50, blank=True, 
        help_text='Optional special instructions')

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.ExerciseManager()

    class Meta:
        verbose_name = 'exercise'
        verbose_name_plural = 'exercises'
        ordering = ('title',)

    def __unicode__(self):
        if self.notes:
            return u'%s (%s)' % (self.title, self.notes)
        return self.title

class WorkoutExercise(models.Model):

    workout = models.ForeignKey(Workout, related_name='exercises',
        help_text='The workout to which this exercise applies')

    item_group = models.PositiveSmallIntegerField(default=1,
        choices=zip(range(1, 13), 'ABCDEFGHIJKL'),
        help_text='Repeatable series identifier')
    item_group_repeats = models.PositiveSmallIntegerField(default=1,
        help_text='How many times this series is repeated')

    effort = models.PositiveSmallIntegerField(default=100,
        help_text='Effort required, generally a weight or distance')
    effort_unit = models.ForeignKey(Unit, default=1, blank=True, null=True,
        help_text='Unit of effort, either empty if it does not apply, like for '
        'push-ups, or something like, "pounds" for weights or weighted runs',
        related_name='+')


    exercise = models.ForeignKey(Exercise, help_text='The exerted movement')

    reps = models.PositiveSmallIntegerField(default=1, 
        help_text='How many times the movement is repeated, or for how far')
    reps_unit = models.ForeignKey(Unit, default=2, blank=True, null=True,
        help_text='Unit of repetition, usually "reps" or "feet" for weighted '
        'runs', related_name='+')

    notes = models.CharField(max_length=50, blank=True, 
        help_text='Optional special instructions')

    order = models.PositiveSmallIntegerField(default=0,
        help_text='The order in which this exercise is to be executed')

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.WorkoutExerciseManager()

    class Meta:
        verbose_name = 'workout exercise'
        verbose_name_plural = 'workout exercises'
        ordering = ('workout', 'item_group', 'order',)

    def detailed_name(self):

        if self.effort_unit:
            effort = u'%s %s ' % (self.effort, self.effort_unit)
        else:
            effort = u''

        if self.reps_unit:
            reps = u', %s %s' % (self.reps, self.reps_unit)
        else:
            reps = u''

        notes = u' (%s)' % self.notes if self.notes else u''

        return u'%(effort)s%(title)s%(reps)s%(notes)s' % {
            'effort' : effort,
            'title' : self.exercise,
            'reps' : reps,
            'notes' : notes
        }

    def __unicode__(self):
        return self.detailed_name()

class WorkoutOfTheDay(models.Model):

    gym = models.ForeignKey(Gym, related_name='wods',
        help_text='The gym that hosts this WOD')
    workout = models.ForeignKey(Workout, related_name='wods',
        help_text='The routine that makes up this WOD')
    day = models.DateField(help_text='The day this WOD is for')

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.WorkoutOfTheDayManager()

    class Meta:
        verbose_name = 'workout of the day'
        verbose_name_plural = 'workouts of the day'
        unique_together = ('gym', 'workout')
        ordering = ('-day', 'gym__order')

    def detailed_name(self):
        return u'%(day)s: %(workout)s' % {
            'workout' : self.workout,
            'day' : self.day.strftime('%a %b %d, %Y')
        }

    def __unicode__(self):
        return self.detailed_name()

class UserWOD(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        help_text='User who performed the WOD')
    wod = models.ForeignKey(WorkoutOfTheDay, 
        help_text='WOD that was performed')
    time = models.TimeField(null=True, blank=True, 
        help_text='Duration of this WOD')
    rounds = models.PositiveSmallIntegerField(null=True, blank=True,
        help_text='Number of rounds performed')

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.UserWODManager()

    class Meta:
        verbose_name = 'user WOD'
        verbose_name_plural = 'user WODs'
        ordering = ('-wod__day', 'user')

    def __unicode__(self):
        return u'"%s" for "%s"' % (self.wod, self.user.username)

class WODExercise(models.Model):

    goal = models.ForeignKey(WorkoutExercise, null=True, blank=True,
        help_text='Target accomplishment, empty if this is extra curricular')
    user_wod = models.ForeignKey(UserWOD, related_name='wod_exercises',
        help_text='WOD to which this exercise was a part of')

    effort = models.PositiveSmallIntegerField(null=True, blank=True,
        help_text='Effort required, generally a weight or distance')
    reps = models.PositiveSmallIntegerField(null=True, blank=True,
        help_text='How many times the movement is repeated, or for how far')
    notes = models.CharField(max_length=50, blank=True, 
        help_text='Optional special instructions')

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.WODExerciseManager()

    class Meta:
        verbose_name = 'user WOD exercise'
        verbose_name_plural = 'user WOD exercises'
        ordering = ('goal__workout', 'goal__item_group', 'goal__order',)

    def detailed_name(self):

        if self.goal.effort_unit:
            effort = self.effort if self.effort is not None else '?'
            effort = u'%s %s ' % (effort, self.goal.effort_unit)
        else:
            effort = u''

        if self.goal.reps_unit:
            reps = self.reps if self.reps is not None else '?'
            reps = u', %s %s' % (reps, self.goal.reps_unit)
        else:
            reps = u''

        notes = u' (%s)' % self.notes if self.notes else u''

        return u'%(effort)s%(title)s%(reps)s%(notes)s' % {
            'effort' : effort,
            'title' : self.goal.exercise,
            'reps' : reps,
            'notes' : notes
        }

    def __unicode__(self):
        return self.detailed_name()

