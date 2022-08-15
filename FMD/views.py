from django.shortcuts import render
from django.views import generic

class HomeView(generic.TemplateView):
    template_name = "home/home.html"

class Home2View(generic.TemplateView):
    template_name = "home/home2.html"