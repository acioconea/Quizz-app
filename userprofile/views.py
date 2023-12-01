from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import random
import string

from userprofile.forms import NewAccountForm, LoginForm


def invite_user(user_id):
    psw = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                               string.ascii_lowercase +
                                               string.digits + '!$%#@') for _ in range(8))
    if (user_instance := User.objects.filter(id=user_id)) and user_instance.exists():
        user_object = user_instance.first()
        user_object.set_password(psw)
        user_object.save()

        content = f"Buna ziua, \n Datele de autentificare sunt: \n username: {user_object.username} \n parola: {psw}"
        msg_html = render_to_string('registration/invite_user.html', {'content_email': content})
        email = EmailMultiAlternatives(subject='Date contact platforma',
                                       body=content,
                                       from_email='contact@platforma.ro',
                                       to=[user_object.email])
        email.attach_alternative(msg_html, 'text/html')
        email.send()
        return True
    return False


# Create your views here.
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
        invite_user(self.object.id)
        return reverse('userprofile:listare_utilizatori')


class ListOfUserView(ListView):
    model = User
    template_name = 'registration/registration_index.html'


class UpdateUserView(UpdateView):
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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to a success page or home
                return redirect('quiz/')
            else:
                # Add an error message for invalid login
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})
