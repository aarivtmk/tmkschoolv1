from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.home, name='home'),
    path('create/', views.create_webpage, name='create_webpage'),
    path('duplicate/<int:page_id>/',
         views.duplicate_webpage, name='duplicate_webpage'),
    path('edit/<int:page_id>/', views.edit_webpage, name='edit_webpage'),
    path('publish/<int:page_id>/', views.publish_webpage, name='publish_webpage'),
    path('page/<int:page_id>/', views.page_detail, name='page_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

]
