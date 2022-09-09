from django import forms
from .models import Community, News
from django_summernote.widgets import SummernoteWidget


class CommuModelForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["title", "name", "content"]
        widgets = {"content": SummernoteWidget()}


class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "thumbnail", "name", "content"]
        widgets = {"content": SummernoteWidget()}
