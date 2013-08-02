from django.contrib import admin

from explodio.common import admin as a
from explodio.xfit import models


class UnitAdmin(admin.ModelAdmin):
    """
    Admin for Units
    """
    list_display = ('title', 'plural')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'plural')

    readonly_fields = ('modified_at', 'created_at',)

class GymLocationAdmin(admin.ModelAdmin):
    """
    Admin for Gym Locations
    """
    list_display = (
        'address_string',
        a.email('email_address'),
        a.phone('phone_number'),
        a.link('website'),
        a.lat_long(('longitude', 'latitude'))
    )
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('active',)
    date_hierarchy = 'created_at'
    search_fields = ('gym__title', 'title',)

    readonly_fields = ('modified_at', 'created_at',)

class GymLocationInline(admin.TabularInline):
    """
    Inline for Gym Locations
    """
    model = models.GymLocation
    extra = 0

class GymAdmin(admin.ModelAdmin):
    """
    Admin for Gyms
    """
    list_display = (
        'title',
        'active',
        a.email('email_address'),
        a.phone('phone_number'),
        a.link('website'),
        'order',
    )
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('active',)
    list_editable = ('order',)
    date_hierarchy = 'created_at'
    search_fields = ('title',)

    inlines = (GymLocationInline,)
    readonly_fields = ('modified_at', 'created_at',)

class WorkoutExerciseInline(admin.TabularInline):
    """
    Inline admin for WorkoutExercises
    """
    model = models.WorkoutExercise 
    extra = 0

class WorkoutAdmin(admin.ModelAdmin):
    """
    Admin for Workouts
    """
    list_display = ('title', 'notes', 'is_hero')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_hero',)
    date_hierarchy = 'created_at'
    search_fields = ('title',)

    inlines = (WorkoutExerciseInline,)
    readonly_fields = ('modified_at', 'created_at',)

class ExerciseAdmin(admin.ModelAdmin):
    """
    Admin for Exercises
    """
    list_display = ('title', 'notes')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    search_fields = ('title',)

    readonly_fields = ('modified_at', 'created_at',)

class WorkoutExerciseAdmin(admin.ModelAdmin):
    """
    Admin for WorkoutExercises
    """
    list_display = (
        'detailed_name',
        a.edit_object_link('workout'),
        a.edit_object_link('exercise'),
        'notes',
        'effort',
        a.edit_object_link('effort_unit'),
        'reps',
        a.edit_object_link('reps_unit'),
    )
    date_hierarchy = 'created_at'
    search_fields = ('exercise__title', 'workout__title',)

    readonly_fields = ('modified_at', 'created_at',)

class WorkoutOfTheDayAdmin(admin.ModelAdmin):
    """
    Admin for WorkoutOfTheDays
    """
    list_display = (
        'detailed_name',
        a.edit_object_link('gym'),
        a.edit_object_link('workout'),
        'day'
    )
    list_filter = ('gym',)
    date_hierarchy = 'day'
    search_fields = ('workout__title',)

    readonly_fields = ('modified_at', 'created_at',)

class WODExerciseAdmin(admin.ModelAdmin):
    """
    Admin for WODExercises
    """
    list_display = (
        'detailed_name',
        a.edit_object_link('goal'),
        'effort',
        'reps',
        'notes'
    )
    date_hierarchy = 'created_at'
    search_fields = ('user_wod__wod__title', 'user_wod__user__username',
        'user_wod__user__email',)

    readonly_fields = ('modified_at', 'created_at',)

class WODExerciseInline(admin.TabularInline):
    """
    Inline admin for WODExercises
    """
    model = models.WODExercise
    extra = 0

class UserWODAdmin(admin.ModelAdmin):
    """
    Admin for UserWODs
    """
    list_display = (
        a.edit_object_link('user'),
        a.edit_object_link('wod'),
    )
    date_hierarchy = 'created_at'
    search_fields = ('wod__title', 'user__username', 'user__email',)

    inlines = (WODExerciseInline,)
    readonly_fields = ('modified_at', 'created_at',)

admin.site.register(models.Unit, UnitAdmin)
admin.site.register(models.Gym, GymAdmin)
admin.site.register(models.GymLocation, GymLocationAdmin)
admin.site.register(models.Workout, WorkoutAdmin)
admin.site.register(models.Exercise, ExerciseAdmin)
admin.site.register(models.WorkoutExercise, WorkoutExerciseAdmin)
admin.site.register(models.WorkoutOfTheDay, WorkoutOfTheDayAdmin)
admin.site.register(models.WODExercise, WODExerciseAdmin)
admin.site.register(models.UserWOD, UserWODAdmin)
