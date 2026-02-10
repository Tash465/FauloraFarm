from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'  # optional, but recommended for namespacing

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True  # redirects logged-in users away from login page
    ), name='login'),
    path('logout/', views.logout_view, name='logout_view'),  
]
