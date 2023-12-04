from django.urls import path
from quiz.views import NewQuizView, QuizView, NewCategoryView, AddQuestionView, UpdateQuestionView, \
    UpdateQuizView
app_name = 'quiz'

urlpatterns = [
    path('new_quiz/', NewQuizView.as_view(), name='quiz_nou'),
    path('', QuizView.as_view(), name='lista_quizuri'),
    path('<int:quiz_id>/add-question/', AddQuestionView.as_view(), name='adaugare_intrebare'),
    path('new_category/', NewCategoryView.as_view(), name='categorie_noua'),
    path('<int:pk>/update-quiz/', UpdateQuizView.as_view(), name='update_quiz'),
    path('<int:pk>/update-question/', UpdateQuestionView.as_view(), name='update_question'),
]
