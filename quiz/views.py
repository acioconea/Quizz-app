from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from quiz.models import Quiz, Question, Choice, Response, Category
from .models import Quiz


class QuizView(ListView):
    model = Quiz
    template_name = 'quiz/quiz_index.html'
    paginate_by = 5


class NewQuizView( CreateView):
    model = Quiz
    fields = ['title', 'category', 'start_time', 'end_time',"creator", 'duration_minutes', 'max_score', 'nr_of_questions']
    template_name = 'forms.html'

    def get_success_url(self):
        return reverse('quiz:adaugare_intrebari')


class NewQuestionView(CreateView):
    model = Question
    fields = ['text']
    template_name = 'forms.html'


class NewCategoryView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'forms.html'

    def get_success_url(self):
        return reverse('quiz:categorie_noua')


