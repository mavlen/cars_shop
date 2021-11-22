from django.urls import path

from .views import (
    register_view, 
    confirm_view, 
    login_view, 
    logout_view,
    reset_password,
    new_password,
    edit_password
)

app_name = 'authe'

urlpatterns = [
    path('register/', register_view, name='registration'),
    path('confirm/<str:code>/', confirm_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset/',reset_password,name='reset'),
    path('reset/<str:code>/',new_password,name='new_password'),
    path('edit_password/',edit_password,name='edit_password'),
]