from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SignUpView, CustomLoginView, CustomPasswordChangeView, CustomPasswordChangeDoneView

app_name = "accounts"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'), 
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]
