import random
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from quiz.models import Category, UserQuizHistory
from .forms import QuestionForm, QuizForm, ChoiceFormSet, CategoryForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from .models import Quiz, Question, Choice, Response


class QuizView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quiz/quiz_index.html'
    paginate_by = 10

    def get_queryset(self):
        return Quiz.objects.order_by('-created_at')


class UserQuizHistoryView(LoginRequiredMixin, ListView):
    model = UserQuizHistory
    template_name = 'quiz/quiz_history.html'
    paginate_by = 10

    def get_queryset(self):
        return UserQuizHistory.objects.filter(user=self.request.user).order_by('-created_at')


class NewCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'forms.html'

    def get_form_kwargs(self):
        data = super(NewCategoryView, self).get_form_kwargs()
        return data

    def get_success_url(self):
        success_url = reverse('quiz:lista_quizuri')
        return success_url


class NewQuizView(LoginRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'forms.html'

    def get_form_kwargs(self):
        data = super(NewQuizView, self).get_form_kwargs()
        data.update({"pk": None})
        return data

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse('quiz:lista_quizuri')
        return success_url


class UpdateQuizView(LoginRequiredMixin, UpdateView):
    model = Quiz
    template_name = 'quiz/update_quiz.html'
    form_class = QuizForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.get_questions()
        return context

    def get_form_kwargs(self):
        data = super(UpdateQuizView, self).get_form_kwargs()
        data.update({"pk": self.kwargs['pk']})
        return data

    def get_success_url(self):
        success_url = reverse_lazy('quiz:lista_quizuri')
        return success_url


class AddQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/add_question.html'
    success_url = reverse_lazy('quiz:update_quiz')

    def form_valid(self, form):
        form.instance.quiz_id = self.kwargs['quiz_id']
        context = self.get_context_data()
        choice_formset = context['choice_formset']

        for choice_form in choice_formset:
            choice_form.instance.question = form.instance

        if form.is_valid() and choice_formset.is_valid():
            self.object = form.save()

            choice_formset.instance = self.object
            choice_formset.save()

            return redirect(self.get_success_url())

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['choice_formset'] = ChoiceFormSet(self.request.POST)
        else:
            data['choice_formset'] = ChoiceFormSet()
        return data

    def get_success_url(self):
        return reverse_lazy('quiz:update_quiz', kwargs={'pk': self.object.quiz_id})


class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'quiz/update_question.html'
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        question = self.get_object()

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context['choice_formset']

        for choice_form in choice_formset:
            choice_form.instance.question = form.instance

        if form.is_valid() and choice_formset.is_valid():
            self.object = form.save()

            choice_formset.instance = self.object
            choice_formset.save()

            return redirect(self.get_success_url())

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['choice_formset'] = ChoiceFormSet(self.request.POST, instance=self.object)
        else:
            data['choice_formset'] = ChoiceFormSet(instance=self.object)
        return data

    def get_success_url(self):
        return reverse('quiz:update_quiz', kwargs={'pk': self.object.quiz_id})


class StartQuizView(View):
    template_name = 'quiz/start_quiz.html'

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        time_up = datetime.combine(datetime.today(), datetime.now().time()) + timedelta(minutes=quiz.duration_minutes)

        user_quiz_history = UserQuizHistory.objects.filter(
            user=request.user,
            quiz=quiz,
            submitted=0,
        ).order_by('-created_at').first() if UserQuizHistory.objects.filter(
            user=request.user,
            quiz=quiz,
            submitted=0,
        ) else UserQuizHistory.objects.create(
            user=request.user,
            quiz=quiz,
            score=0,
            created_at=timezone.now(),
            submitted=0, )

        user_quiz_history.save()

        questions = quiz.get_questions().order_by(F('id').desc())
        questions = list(questions)
        random.shuffle(questions)
        questions = questions[:quiz.nr_of_questions] if len(questions) >= quiz.nr_of_questions else questions
        selected_question_ids = [question.id for question in questions]
        request.session['selected_question_ids'] = selected_question_ids

        total_score = quiz.max_score
        score_per_question = total_score / len(questions) if len(questions) > 0 else 0.0

        context = {
            'quiz': quiz,
            'questions': questions,
            'total_score': total_score,
            'score_per_question': score_per_question,
            'user_quiz_history': user_quiz_history,
            'time_up': time_up,
        }

        return render(request, self.template_name, context)


class SubmitQuizView(View):
    template_name = 'quiz/submit_quiz.html'

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        selected_question_ids = request.session.get('selected_question_ids', [])
        questions = quiz.get_questions().filter(id__in=selected_question_ids)

        user_quiz_history = UserQuizHistory.objects.filter(
            user=request.user,
            quiz=quiz,
            submitted=0,
        ).order_by('-created_at').first()

        user_responses = []
        total_score = 0

        for question in questions:
            choice_ids = request.POST.getlist(f'choice_{question.id}', [])

            correct_choices = question.choice_set.filter(is_correct=True).values_list('id', flat=True)

            if set(map(int, choice_ids)) == set(correct_choices):
                question_score = quiz.max_score / len(questions)
                total_score += question_score
            else:
                question_score = 0

            response = Response(
                user=request.user,
                quiz=user_quiz_history,
                question=question,
                score=question_score
            )
            response.save()

            response.selected_answer.set(Choice.objects.filter(id__in=choice_ids))

            user_responses.append(response)

        user_quiz_history.score = total_score
        user_quiz_history.submitted = True
        user_quiz_history.save()

        context = {
            'user_quiz_history': user_quiz_history,
            'user_responses': user_responses,
            'total_score': total_score,
        }

        return render(request, self.template_name, context)


class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'quiz/quiz_confirm_delete.html'
    success_url = reverse_lazy('quiz:lista_quizuri')


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'quiz/question_confirm_delete.html'
    success_url = reverse_lazy('quiz:update_quiz')

    def get_success_url(self):
        return reverse_lazy('quiz:update_quiz', kwargs={'pk': self.object.quiz_id})


class QuizHistoryView(LoginRequiredMixin, ListView):
    model = UserQuizHistory
    template_name = 'quiz/quiz_results.html'
    paginate_by = 10

    def get(self, request, pk):
        quiz_history_list = UserQuizHistory.objects.filter(quiz_id=pk)

        context = {
            'quiz_history_list': quiz_history_list,
            'quiz_id': pk,
        }

        return render(request, self.template_name, context)
