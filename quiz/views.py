from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from quiz.forms import QuizForm
from quiz.models import Quiz,Question,Choice,Response


class QuizView(ListView):

    model = Quiz
    template_name = 'quiz/quiz_index.html'
    paginate_by = 5


class NewQuizView(CreateView):

    model = Quiz
    fields = ['title', 'category','start_time','end_time','duration_minutes','max_score','nr_of_questions']
    template_name = 'forms.html'

    def get_success_url(self):
        return reverse('quiz:quiz_nou')
#
#
# class UpdateLocationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Location
#     fields = ['city', 'country']
#     template_name = 'forms.html'
#
#     def test_func(self):
#         user_location = self.request.user.userextend.location.id
#         if ((get_location := Location.objects.filter(id=self.kwargs['pk'])) and
#                 get_location.exists() and
#                 user_location == get_location.first().id):
#             return True
#         return False
#
#     def get_success_url(self):
#         return reverse('aplicatie1:lista_locatii')
#
#
# @login_required
# def deactivate_location(request, pk):
#     Location.objects.filter(id=pk).update(active=False)
#     return redirect('aplicatie1:lista_locatii')
#
#
# @login_required
# def activate_location(request, pk):
#     Location.objects.filter(id=pk).update(active=True)
#     return redirect('aplicatie1:lista_locatii')
class NewQuestionView(CreateView):

    model = Question
    fields = ['text']
    template_name = 'forms.html'

    def create_quiz(request):
        if request.method == 'POST':
            form = QuizForm(request.POST)
            if form.is_valid():
                quiz = form.save(commit=False)
                quiz.created_by = request.user
                quiz.save()
                return redirect('quiz_detail', quiz_id=quiz.id)
        else:
            form = QuizForm()

        quizzes = Quiz.objects.filter(created_by=request.user)
        return render(request, 'create_quiz.html', {'form': form, 'quizzes': quizzes})

    @login_required
    def quiz_detail(request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.get_questions()
        return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions})