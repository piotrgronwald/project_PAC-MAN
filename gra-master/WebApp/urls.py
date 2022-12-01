"""WebApp URL Configuration

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
from GameRank.models import GameRank1
from GameRank.admin import WebAppAdmin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from GameRank.views import gamerank_list, SignUpView

admin.site.register(GameRank1, WebAppAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gamerank_list', gamerank_list, name='gamerank_list'),
    path('accounts/login/', LoginView.as_view(template_name='form.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/sign_up', SignUpView.as_view(), name='sign_up'),
    path('game/', include('Game.urls'))
]
