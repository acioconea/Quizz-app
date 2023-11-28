from django.urls import path

from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('new_quiz/', views.NewQuizView.as_view(), name='quiz_nou'),
    path('', views.QuizView.as_view(), name='lista_quizuri'),
    path('add_questions/', views.NewQuestionView.as_view(), name='adauga_intrebari'),
    # path('<int:pk>/editare/', views.UpdateUserView.as_view(), name='editare_quiz'),
    # path('quiz_list/', views.ListOfUserView.as_view(), name='listare_quizuri'),
]