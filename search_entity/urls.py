from django.urls import path
from . import views

app_name = 'search_entity'

urlpatterns = [
    path('search-entity/', views.search_entity, name='search_entity'),
    path('upload-file/', views.upload_file, name='upload_file')
]
