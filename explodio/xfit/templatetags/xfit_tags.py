from django import template

register = template.Library()


@register.filter
def pluralize_unit(unit, amount):
    if amount != 1:
        return unit.plural
    return unit.title

@register.filter
def effort_unit(workout):
    return pluralize_unit(workout.effort_unit, workout.effort)

@register.filter
def reps_unit(workout):
    return pluralize_unit(workout.reps_unit, workout.reps)