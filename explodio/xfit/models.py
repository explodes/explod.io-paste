from django.conf import settings
from django.db import models

from explodio.xfit import managers
from explodio.xfit.templatetags import xfit_tags


class Unit(models.Model):
    """
    Model representing a unit of work, i.e. Pound, Meter, Second
    """

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
    """
    Gym hosting certain WODs
    """

    title = models.CharField(max_length=50, help_text='Title of this gym')
    slug = models.SlugField(max_length=50, unique=True,
        help_text='Used for URLs')
    active = models.BooleanField(default=True, help_text='Un-check to disable '
        'this gym on the website')

    email_address = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

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

class GymLocation(models.Model):
    """
    Model for a physical location of a Gym
    """

    gym = models.ForeignKey(Gym, related_name='locations')

    title = models.CharField(max_length=50, help_text='Title of this location')
    slug = models.SlugField(max_length=50, help_text='Used for URLs')
    active = models.BooleanField(default=True, help_text='Un-check to disable '
        'this location on the website')

    address1 = models.CharField(max_length=75, null=True, blank=True)
    address2 = models.CharField(max_length=75, null=True, blank=True)
    city = models.CharField(max_length=75, null=True, blank=True)
    state = models.CharField(max_length=75, null=True, blank=True)
    postal_code = models.CharField(max_length=75, null=True, blank=True)
    country = models.CharField(max_length=75, null=True, blank=True)

    latitude = models.DecimalField(max_digits=12, decimal_places=9, null=True,
        blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, null=True,
        blank=True)

    email_address = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.GymLocationManager()

    class Meta:
        verbose_name = 'gym location'
        verbose_name_plural = 'gym locations'
        unique_together = (
            ('gym', 'slug'),
        )

    def address_string(self):
        return u', '.join(filter(bool, (
            self.address1,
            self.address2,
            self.city,
            self.state,
            self.postal_code,
            self.country,
        )))

    def __unicode__(self):
        return self.address_string()

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

    high_round_divisor = models.PositiveSmallIntegerField(default=1,
        help_text='When the number of rounds is high, filling them all out is '
            'a real pain. Put in the notes "32 rounds" and put 32 in this box. '
            'Recorded reps or distance will be divided by 32, per round, in '
            'that case.')

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
        notes = u' (%s)' % self.notes if self.notes else u''
        return u'%s%s' % (self.title, notes)

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
        help_text='Effort required, generally a weight or distance. '
            '0 indicates "max."')
    effort_unit = models.ForeignKey(Unit, default=1, blank=True, null=True,
        help_text='Unit of effort, either empty if it does not apply, like for '
        'push-ups, or something like, "pounds" for weights or weighted runs',
        related_name='+')

    exercise = models.ForeignKey(Exercise, help_text='The exerted movement')

    reps = models.PositiveSmallIntegerField(default=1, 
        help_text='How many times the movement is repeated, or for how far. '
            '0 indicates "max."')
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

    def unit_string(self, amount, unit):
        if unit:
            amount = 'max' if amount == 0 else amount
            unit = xfit_tags.pluralize_unit(unit, amount)
            return u'%s %s' % (amount, unit)
        return u''

    def detailed_name(self):

        effort = self.unit_string(self.effort, self.effort_unit)
        # example: 5000 meter\sRun
        effort = u'%s ' % effort if effort else effort

        reps = self.unit_string(self.reps, self.reps_unit)
        # example: Push Ups, 100 reps
        reps = u', %s' % reps if reps else reps

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

    @models.permalink
    def get_absolute_url(self):
        day = self.day
        return 'xfit:index', (), {
            'year': day.year,
            'month': day.month,
            'day': day.day,
        }

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

    @models.permalink
    def get_absolute_url(self):
        day = self.wod.day
        return 'xfit:index', (), {
            'year': day.year,
            'month': day.month,
            'day': day.day,
        }

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

