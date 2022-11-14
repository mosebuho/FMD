from django import forms
from .models import Community, News, Column, Event
from django_summernote.widgets import SummernoteWidget


class CommuModelForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목을 입력해주세요."}),
            "content": SummernoteWidget(),
        }


class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "thumbnail", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목을 입력해주세요."}),
            "content": SummernoteWidget(),
        }


class ColumnModelForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ["title", "thumbnail", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목을 입력해주세요."}),
            "content": SummernoteWidget(),
        }


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "thumbnail", "content", "start", "end"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목을 입력해주세요."}),
            "content": SummernoteWidget(),
            "start": forms.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "시작일",
                    "type": "date",
                },
            ),
            "end": forms.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "종료일",
                    "type": "date",
                },
            ),
        }
