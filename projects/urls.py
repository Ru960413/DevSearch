from django.urls import path
from . import views

urlpatterns = [
    # path takes 3 parameters, first: the path, second: the function which will then trigger HttpResponse
    
    # setting project page to the default page
    path('',  views.projects, name='projects'),
    # <str:pk> : a dynamic info can be passed in
    path('project/<str:pk>/',  views.project, name='project'),

    path('create-project/', views.createProject, name="create-project"),
    
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),

    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
]