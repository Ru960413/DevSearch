"""devsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from projects.views import projects
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # include all the urls from urls.py from the projects folder
    path('projects/', include('projects.urls')),
    path('', include('users.urls')), 
    path('api/', include('api.urls')),

    
    # we are using as_view() here because PasswordResetView is a class, not a function,
    # so we point the URL to the as_view() class method instead, which provides a function-like entry to class-based views
    # as_view() is a class method that returns a callable view that takes a request and returns a response
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    path('rest_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    
    # uidb64: The user’s id encoded in base 64. token: Token to check that the password is valid.
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),

]

# connecting media url to media root, so django knows where to find user uploaded images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# 1 - User submits email for reset              //PasswordResetView.as_view()           //name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view()        //name="password_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfirmView()            //name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView.as_view()   //name="password_reset_complete"