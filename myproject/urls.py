"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from myapp import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('myapp.urls')),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('add_note', views.add_note, name='add_note'),
    path('get_user_notes', views.get_user_notes, name='get_user_notes'),
    path('update_note/<int:note_id>', views.update_note, name='update_note'),
    path('delete_note/<int:note_id>', views.delete_note, name='delete_note'),
    path('login', views.login, name='login'),
    path('check_auth_status', views.check_auth_status, name='check_auth_status'),
    path('logout_user', views.logout_user, name='logout_user'),



]
