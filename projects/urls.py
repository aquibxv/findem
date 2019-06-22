from django.urls import path, include
from . import views

# url - 'project/'
urlpatterns = [
    path('search', views.search, name='search_project'),
    path('create', views.create, name='create'),
    path('view/<int:project_id>', views.project_view, name='project_view'),
    path('<int:project_id>', views.project_delete, name='project_delete'),
    path('edit/<int:project_id>', views.project_edit, name='project_edit'),
]