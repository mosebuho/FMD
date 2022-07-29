from django.shortcuts import render
from django.views import generic
from .models import Board

class BoardlistView(generic.ListView):
    template_name = "board/board.html"
    queryset = Board.objects.all()
    context_object_name = "boards"