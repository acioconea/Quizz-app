from django.urls import path

from quiz import views
from quiz.views import NewQuizView, QuizView, NewQuestionView, NewCategoryView

app_name = 'quiz'

urlpatterns = [
    path('new_quiz/', NewQuizView.as_view(), name='quiz_nou'),
    path('', QuizView.as_view(), name='lista_quizuri'),
    path('<int:pk>/add_questions/', NewQuestionView.as_view(), name='adauga_intrebari'),
    path('new_category/', NewCategoryView.as_view(), name='categorie_noua'),
    # path('<int:pk>/editare/', views.UpdateUserView.as_view(), name='editare_quiz'),
    # path('quiz_list/', views.ListOfUserView.as_view(), name='listare_quizuri'),
]