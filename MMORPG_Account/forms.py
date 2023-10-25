#forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.models import Group
from .models import UsersAuth



class EditProfileForm(forms.ModelForm):
    GROUP_CHOICES = (
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('damage_dealers', 'ДД'),
        ('dealers', 'Торговцы'),
        ('gildmasters', 'Гилдмейстеры'),
        ('quest_givers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion_makers', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний'),
    )
    group = forms.ChoiceField(choices=GROUP_CHOICES, label='Группа', required=True)

    class Meta:
        model = UserProfile
        fields = ['group']
    def save(self, commit=True):
        instance = super(EditProfileForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

class AuthCodeForm(forms.Form):
    code = forms.IntegerField(label="Код регистрации")



