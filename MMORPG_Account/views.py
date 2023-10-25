#view.py
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView, FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.views.generic import CreateView


from .models import UsersAuth
from .forms import EditProfileForm, AuthCodeForm
import random

class AccountProfile(LoginRequiredMixin, FormView):
    template_name = 'allauth/account/profile.html'
    form_class = AuthCodeForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UsersAuth.objects.filter(user=self.request.user).exists():
                return super().dispatch(request, *args, **kwargs)
            return HttpResponseRedirect(reverse('auth_code'))
        else:
            return HttpResponseRedirect(reverse('index'))

    def form_valid(self, form, **kwargs):
        global code_not_correct
        if form.cleaned_data['code'] == UsersAuth.objects.get(user=self.request.user).code:
            Group.objects.get(name='AuthUsers').user_set.add(self.request.user)
        else:
            code_not_correct = "Введен неверный код подтверждения"
        return HttpResponseRedirect(reverse('account_profile'))

    def get_context_data(self, **kwargs):
        context = super(AccountProfile, self).get_context_data(**kwargs)
        context['code_not_correct'] = code_not_correct
        if self.request.user.groups.filter(name='AuthUsers').exists():
            context['auth'] = True
        else:
            context['auth'] = False
        return context
        context['user_group'] = None
        if self.request.user.is_authenticated:
            context['user_group'] = self.request.user.groups.first()
        return context



@login_required
def auth_code(request):
    global code_not_correct
    code_not_correct = ""

    if not UsersAuth.objects.filter(user=request.user).exists():
        add_user = UsersAuth()
        add_user.user = request.user
        add_user.save()

    user = UsersAuth.objects.get(user=request.user)
    user.code = random.randint(1000, 9999)
    user.save()
    send_mail(
        subject='MMORPG Fans: подтверждение e-mail',
        message=f'Доброго дня, {request.user}! Для подтверждения регистрации, введите код {user.code} на '
                f'странице регистрации\nhttp://127.0.0.1:8000/MMORPG_Account/profile',
        from_email='zimina.nina202020@yandex.ru',
        recipient_list=[request.user.email, ],
    )
    return HttpResponseRedirect(reverse('account_profile'))

class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    success_url = '/MMORPG_Account/profile'
    template_name = 'allauth/account/update_profile.html'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
          queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class RegisterView(CreateView):
    form_class = EditProfileForm
    template_name = 'allauth/account/register.html'
    success_url = '/index/'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        group = Group.objects.get(name=form.cleaned_data['group'])
        user.groups.add(group)
        login(self.request, user)
        return response
