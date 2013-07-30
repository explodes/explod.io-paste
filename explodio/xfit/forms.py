from django import forms

from explodio.common.forms import FormHelpersMixin
from explodio.xfit import models


class TimeForm(forms.Form):
    time = forms.TimeField()

class WODExerciseForm(forms.ModelForm, FormHelpersMixin):

    CLONE_FIELDS = ('effort', 'reps', 'notes')
    REQUIRE_IF_CLONE = (
        ('effort', 'effort_units'),
        ('reps', 'reps_units'),
    )

    class Meta:
        fields = WODExerciseForm.CLONE_FIELDS
        model = models.WODExercise

    def __init__(self, goal, *args, **kwargs):
        super(WODExerciseForm, self).__init__(*args, **kwargs)

        for field in WODExerciseForm.CLONE_FIELDS:
            self.set_default(field, getattr(goal, field))

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
