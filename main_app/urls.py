from django.urls import path
from rest_framework.routers import DefaultRouter

from main_app import views

router = DefaultRouter()
router.register(r'projects', views.ProjectList, basename='projects')
router.register(r'news', views.NewsList, basename='news')
router.register(r'categories', views.CategoriesList, basename='categories')

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.AccountsList.as_view(), name='accounts'),
    path('founders/', views.FoundersList.as_view(), name='founders'),
    path('media/', views.MediaList.as_view(), name='media'),
    path('projects/<int:pk>/related_projects/', views.RelatedProjects.as_view()),
    *router.urls,
]
