from django.urls import path

from main_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts', views.AccountsList.as_view()),
    path('categories', views.CategoriesList.as_view()),
    path('projects', views.ProjectList.as_view()),
]
