from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse

class LoginView(generic.ListView):
    template_name = 'textbookFinder/login.html'

    def get_queryset(self):
        return
