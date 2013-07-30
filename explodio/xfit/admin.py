from django.contrib import admin

from explodio.xfit import models


class GymAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('active',)
    date_hierarchy = 'created_at'
    search_fields = ('title',)

    readonly_fields = ('modified_at', 'created_at',)

class WorkoutExerciseInline(admin.TabularInline):
    model = models.WorkoutExercise 
    extra = 0

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_hero')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_hero',)
    date_hierarchy = 'created_at'
    search_fields = ('title',)

    inlines = [WorkoutExerciseInline]
    readonly_fields = ('modified_at', 'created_at',)

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'notes')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    search_fields = ('title',)

    readonly_fields = ('modified_at', 'created_at',)

class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('detailed_name', 'workout', 'exercise', 'effort',
        'effort_unit', 'reps', 'reps_unit')
    date_hierarchy = 'created_at'
    search_fields = ('exercise__title', 'workout__title',)

    readonly_fields = ('modified_at', 'created_at',)

class WorkoutOfTheDayAdmin(admin.ModelAdmin):
    list_display = ('detailed_name', 'gym', 'workout', 'day')
    list_filter = ('gym',)
    date_hierarchy = 'day'
    search_fields = ('workout__title',)

    readonly_fields = ('modified_at', 'created_at',)

class WODExerciseAdmin(admin.ModelAdmin):
    list_display = ('detailed_name', 'goal', 'effort', 'reps')
    date_hierarchy = 'created_at'
    search_fields = ('user_wod__wod__title', 'user_wod__user__username',
        'user_wod__user__email',)

    readonly_fields = ('modified_at', 'created_at',)

class WODExerciseInline(admin.TabularInline):
    model = models.WODExercise
    extra = 0

class UserWODAdmin(admin.ModelAdmin):
    list_display = ('user', 'wod')
    date_hierarchy = 'created_at'
    search_fields = ('wod__title', 'user__username', 'user__email',)

    inlines = [WODExerciseInline]
    readonly_fields = ('modified_at', 'created_at',)

admin.site.register(models.Gym, GymAdmin)
admin.site.register(models.Workout, WorkoutAdmin)
admin.site.register(models.Exercise, ExerciseAdmin)
admin.site.register(models.WorkoutExercise, WorkoutExerciseAdmin)
admin.site.register(models.WorkoutOfTheDay, WorkoutOfTheDayAdmin)
admin.site.register(models.WODExercise, WODExerciseAdmin)
admin.site.register(models.UserWOD, UserWODAdmin)
