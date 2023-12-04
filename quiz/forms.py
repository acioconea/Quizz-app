from django import forms
from django.forms import TextInput, Select, DateField, NumberInput, DateInput, inlineformset_factory
from django.http import request
from django.shortcuts import redirect

import quiz
from quiz.models import Quiz, Question, Choice, Category


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['title', 'category', 'start_time', 'end_time','duration_minutes', 'max_score', 'nr_of_questions']

        widgets = {
            "title": TextInput(attrs={"placeholder": "Title", "class": "form-control"}),
            "category": Select(attrs={"placeholder": "Category", "class": "form-control"}),
            "start_time": DateInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "end_time": DateInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "duration_minutes": NumberInput(attrs={"class": "form-control"}),
            "max_score": NumberInput(attrs={"placeholder": 100, "class": "form-control"}),
            "nr_of_questions": NumberInput(attrs={"placeholder": 5, "class": "form-control"}),
        }

    def __init__(self, pk, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.pk = pk
        # redirect('create_question', quiz_id=pk)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

        widgets = {
            "text": TextInput(attrs={"placeholder": "Text", "class": "form-control"})}

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        if self.pk is not None:
            self.choice_formset = ChoiceFormSet(instance=self.instance)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=4)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            " name": TextInput(attrs={"placeholder": "Category", "class": "form-control"}),
        }
