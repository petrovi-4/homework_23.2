import random
import secrets

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, TemplateView, UpdateView, FormView

from config import settings
from users.forms import UserRegisterForm, PasswordRecoveryForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:expectation')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_urlsafe(16)
        print('Token:', user.token)
        user.save()
        email = user.email
        token = user.token
        url = f'http://127.0.0.1:8000/users/verification/{token}'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return super().form_valid(form)


class VerificationView(TemplateView):
    template_name = 'users/verification.html'
    extra_context = {
        'title': 'Поздравляем! Вы успешно зарегистрировались'
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = self.kwargs.get('token')
        try:
            user = User.objects.get(token=token)
            user.is_active = True
            user.save()
            context['success'] = True
        except User.DoesNotExist:
            context['success'] = False
        return self.render_to_response(context)


def expectation(request):
    context = {
        'title': 'Подтверждения регистрации'
    }
    return render(request, 'users/expectation.html', context)


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserRegisterForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    send_mail(
        subject='Запрос нового пароля',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:index'))


class PasswordRecoveryView(FormView):
    template_name = 'users/password_recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        length = 12
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        password = get_random_string(length, alphabet)
        user.set_password(password)
        user.save()
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль: {password}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)
