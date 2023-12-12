from django.urls import path
from quiz.views import NewQuizView, QuizView, NewCategoryView, AddQuestionView, UpdateQuestionView, \
    UpdateQuizView, StartQuizView, SubmitQuizView, QuizDeleteView, QuestionDeleteView, home, UserQuizHistoryView

app_name = 'quiz'

urlpatterns = [
    path('new_quiz/', NewQuizView.as_view(), name='quiz_nou'),
    path('quiz_list', QuizView.as_view(), name='lista_quizuri'),
    path('quiz_history', UserQuizHistoryView.as_view(), name='istoric_quiz'),
    path('<int:quiz_id>/add-question/', AddQuestionView.as_view(), name='adaugare_intrebare'),
    path('new_category/', NewCategoryView.as_view(), name='categorie_noua'),
    path('<int:pk>/update-quiz/', UpdateQuizView.as_view(), name='update_quiz'),
    path('<int:pk>/update-question/', UpdateQuestionView.as_view(), name='update_question'),
    path('<int:quiz_id>/start/', StartQuizView.as_view(), name='start_quiz'),
    path('<int:quiz_id>/submit/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('', home, name='home'),
]
