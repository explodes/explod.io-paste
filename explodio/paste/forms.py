from datetime import timedelta

from django import forms
from django.utils.datetime_safe import datetime

from explodio.paste import models as paste


EXPIRES_CHOICES = (
    ('1h', 'One Hour'),
    ('1d', 'One Day'),
    ('2d', 'Two Days'),
    ('14d', 'Two Weeks'),
    ('60d', 'Two Months'),
    ('1y', 'One Year'),
    ('inf', 'Never'),
)


class PasteForm(forms.ModelForm):

    expiration = forms.ChoiceField(choices=EXPIRES_CHOICES)

    class Meta:
        model = paste.Paste
        fields = ('title', 'language', 'style', 'code')

    def get_expiration_date(self):
        expiry = self.cleaned_data['expiration']

        expiration_date = datetime.now()

        if expiry == '1h':
            expiration_date += timedelta(hours=1)
        elif expiry == '1d':
            expiration_date += timedelta(days=1)
        elif expiry == '2d':
            expiration_date += timedelta(days=2)
        elif expiry == '14d':
            expiration_date += timedelta(days=14)
        elif expiry == '60d':
            expiration_date += timedelta(days=60)
        elif expiry == '1y':
            expiration_date += timedelta(days=365)
        elif expiry == 'inf':
            expiration_date += timedelta(days=365*250)
        else:
            raise ValueError('Unknown expiration date extension')

        return expiration_date

    def save(self, ip_address, commit=True):
        instance = super(PasteForm, self).save(commit=False)
        instance.ip_address = ip_address
        instance.expires_at = self.get_expiration_date()
        if commit:
            instance.save()
        return instance
