from common.views import TitleMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from products import models
from users.forms import UserLoginForm, UserRegForm, UserProfileForm
from users.models import User


class UserCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = '%(first_name)s %(last_name)s You are successfully registered!'
    title = 'Registration'


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserUpdateView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(
            {'bucket': models.Bucket.objects.filter(user=self.object)}
        )
        return data

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {
#         'title': 'Profile',
#         'form': form,
#         'bucket': models.Bucket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/profile.html', context)


# def registration(request):
#     if request.method == 'POST':
#         data = request.POST
#         form = UserRegForm(data=data)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Пользователь зарегистрирован!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegForm()
#     return render(request, 'users/registration.html', {'form': form})

# def login(request):
#     if request.method == 'POST':
#         data = request.POST
#         form = UserLoginForm(data=data)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('users:profile'))
#             else:
#                 return PermissionDenied()
#     else:
#         form = UserLoginForm()
#     context = {'form': form, 'title': 'Authorization'}
#     return render(request, 'users/login.html', context)
