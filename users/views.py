from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.views.generic import FormView

from .forms import CustomUserCreationForm

class SignUp(FormView):
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(SignUp, self).form_valid(form)
