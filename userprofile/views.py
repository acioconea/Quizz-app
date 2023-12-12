from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from userprofile.forms import NewAccountForm, LoginForm


class CreateNewAccountView(CreateView):
    model = User
    template_name = 'forms.html'
    # fields = ['first_name', 'last_name', 'username', 'email']
    form_class = NewAccountForm

    def get_form_kwargs(self):
        data = super(CreateNewAccountView, self).get_form_kwargs()
        data.update({"pk": None})
        return data

    def get_success_url(self):
        return reverse('quiz:home')


class ListOfUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'registration/registration_index.html'


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'forms.html'
    # fields = ['first_name', 'last_name', 'username', 'email']
    form_class = NewAccountForm

    def get_form_kwargs(self):
        data = super(UpdateUserView, self).get_form_kwargs()
        data.update({"pk": self.kwargs['pk']})
        return data

    def get_success_url(self):
        return reverse('userprofile:listare_utilizatori')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('quiz/')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})
