from django import forms
from django.forms import TextInput, Select, DateField, NumberInput
from django.http import request
from django.shortcuts import redirect

import quiz
from quiz.models import Quiz, Question, Choice


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['title', 'category', 'start_time', 'end_time', 'duration_minutes', 'max_score', 'nr_of_questions']

        widgets = {
            "title": TextInput(attrs={"placeholder": "Title", "class": "form-control"}),
            "category": Select(attrs={"placeholder": "Category", "class": "form-control"}),
            "start_time": DateField(),
            "end_time": DateField(),
            "duration_minutes": NumberInput(attrs={"class": "form-control"}),
            "max_score": NumberInput(attrs={"placeholder": 100, "class": "form-control"}),
            "nr_of_questions": NumberInput(attrs={"placeholder": 5, "class": "form-control"}),
        }

    def __init__(self, pk, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.pk = pk
        self.creator=request.user.pk
        # redirect('create_question', quiz_id=pk)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            "text": TextInput(attrs={"placeholder": "Question", "class": "form-control"}),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            "text": TextInput(attrs={"placeholder": "Choice", "class": "form-control"}),
        }