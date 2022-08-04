from django.shortcuts import render
from django.views import generic
from .models import Community

class BoardlistView(generic.ListView):
    template_name = "board/community.html"
    queryset = Community.objects.all()
    context_object_name = "posts"