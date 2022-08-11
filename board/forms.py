from django import forms
from .models import Community
from django_summernote.widgets import SummernoteWidget

class CommuModelForm(forms.ModelForm):
    options = (
        ("free", "자유"),
        ("info", "정보"),
    )
    name = forms.ChoiceField(widget=forms.Select(), choices=options)
    class Meta:
        model = Community
        fields = ["title", "name", "content"]
        widgets = {"content": SummernoteWidget()}
