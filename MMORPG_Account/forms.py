#forms.py
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User




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
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class AuthVerifiCodeForm(forms.Form):
    code = forms.IntegerField(label="Код регистрации")



