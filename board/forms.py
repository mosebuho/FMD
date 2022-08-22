from django import forms
from .models import Community, Comment
from django_summernote.widgets import SummernoteWidget


class CommuModelForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["title", "name", "content"]
        widgets = {"content": SummernoteWidget()}

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]