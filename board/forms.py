from django import forms
from .models import Community, News


class CommuModelForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["title", "name", "content"]


class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "thumbnail", "name", "content"]
    