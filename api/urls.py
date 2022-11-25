from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns =[
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),

    # let us generate a Json Web token
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # refresh(i.e. generate a new token), when the old token has expired
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('remove-tag/', views.removeTag),
]