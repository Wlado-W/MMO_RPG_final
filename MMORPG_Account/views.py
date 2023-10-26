#view.py
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView, FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from datetime import datetime

from .models import UserAuthenticationCode
from .forms import EditProfileForm, AuthVerifiCodeForm
import random

class AccountProfile(LoginRequiredMixin, FormView):
    template_name = 'allauth/account/profile.html'
    form_class = AuthVerifiCodeForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UserAuthenticationCode.objects.filter(user=self.request.user).exists():
                return super().dispatch(request, *args, **kwargs)
            return HttpResponseRedirect(reverse('auth_code'))
        else:
            return HttpResponseRedirect(reverse('index'))

    def form_valid(self, form, **kwargs):
        code_not_correct = None
        if form.cleaned_data['code'] == UserAuthenticationCode.objects.get(user=self.request.user).code:
            Group.objects.get(name='UserAuthenticationCode').user_set.add(self.request.user)
        else:
            code_not_correct = "Введен неверный код подтверждения, попробуйте еще раз."
        return HttpResponseRedirect(reverse('account_profile'))

    def get_context_data(self, **kwargs):
        context = super(AccountProfile, self).get_context_data(**kwargs)
        if self.request.user.groups.filter(name='UserAuthenticationCode').exists():
            context['auth'] = True
        else:
            context['auth'] = False
        return context

@login_required
def auth_code(request):
    if not UserAuthenticationCode.objects.filter(user=request.user).exists():
        add_user = UserAuthenticationCode()
        add_user.user = request.user
        add_user.save()

    user = UserAuthenticationCode.objects.get(user=request.user)
    user.code = random.randint(1000, 9999)
    user.save()

    current_time = datetime.now().time()
    if current_time.hour < 12:
        greeting = "Доброе утро"
    elif current_time.hour < 17:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    send_mail(
        subject='MMORPG Fans: подтверждение e-mail',
        message=f'{greeting}, {request.user}! Для подтверждения регистрации, введите код {user.code} на '
                f'странице регистрации\n{reverse("profile_accounts")}',
        from_email='zimina.nina202020@yandex.ru',
        recipient_list=[request.user.email, ],
    )
    return HttpResponseRedirect(reverse('profile_accounts'))

class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    success_url = 'profile_accounts'
    template_name = 'allauth/account/edit_profile.html'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

