

## this is my myapps uls
from django.urls import path
from . import views

urlpatterns = [
    path('unlock_owner/<int:id>/', views.unlock_owner, name='unlock_owner'),
    path('lock_owner/<int:id>/', views.lock_owner, name='lock_owner'),
    path('', views.loading, name='loading'),
    path('register', views.register, name='register'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('login_user', views.login_user, name='login_user'),
    path('view_record/<int:id>/', views.view_record, name='view_record'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('create/', views.createUser, name='create'),
    path('index', views.index, name='index'),
    path('logList/<int:id>', views.logList, name='logList'),

]
