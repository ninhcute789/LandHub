from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verification-sent/', views.verification_sent, name='verification_sent'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('profile/update/', views.update_profile, name='update_profile'),
]
