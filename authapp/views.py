
from django.conf import settings
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from authapp.models import User
from basketapp.models import Basket
from authapp.forms import UserRegisterForm, UserLoginForm, UserProfileForm, UserProfileEditForm


class LoginListView(LoginView):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context


class RegisterListView(FormView):
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(RegisterListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, 'Вы успешно зарегистрировались!'
                                          ' Для авторизации профиля пройдите по ссылке направленной '
                                          'на электронную почту ')
                return redirect(self.success_url)

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def send_verify_mail(self, user):
        verify_link = reverse_lazy('authapp:verify', args=[user.email, user.activation_key])

        title = f'Для активации учетной записи {user.username} пройдите по ссылке'

        messages = f'Для подтверждения учетной записи {user.username} пройдите по ссылке: \n{settings.DOMAIN_NAME}' \
                   f'{verify_link}'

        return send_mail(title, messages, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expires():
                user.is_active = True
                user.save()
                auth.login(self, user)
                return render(self, 'mainapp/index.html')
            else:
                print(f'error activation user: {user}')
                return render(self, 'authapp/verification.html')
        except Exception as e:
            print(f'error activation user : {e.args}')
            return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class ProfileFormView(FormView):
    form_class = UserProfileForm
    form_class_second = UserProfileEditForm
    success_url = reverse_lazy('auth:profile')
    template_name = 'authapp/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Профиль'
        context['profile_form'] = self.form_class_second(instance=self.request.user.userprofile)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileFormView, self).dispatch(request, *args, **kwargs)


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        edit_form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=user.userprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            user.userprofile.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {
            'form': edit_form,
            'profile_form': profile_form,
        })


# @transaction.atomic
# def edit(request):
#     title = 'редактирование'
#
#     if request.method == 'POST':
#         edit_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
#         profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.userprofile)
#
#         if edit_form.is_valid() and profile_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#     else:
#         edit_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
#         profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.userprofile)
#     context = {
#         'title': title,
#         'form': edit_form,
#         'profile_form': profile_form,
#     }
#     return render(request, 'authapp/profile.html', context)