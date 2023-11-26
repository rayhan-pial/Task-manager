from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserProfileview, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView
from to_do.views import TodoListCreateView, TodoListretriveUpdateDestroyView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileview.as_view(), name='profile'),
    path('changepass/', UserChangePasswordView.as_view(), name='changepass'),
    path('send-reset-pass-email/', SendPasswordResetEmailView.as_view(), name='send-reset-pass-email'),
    path('reset-pass/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-pass'),
    path('to-do/', TodoListCreateView.as_view(), name='todo'),
    path('to-do/retrive_update_delete/<int:id>/', TodoListretriveUpdateDestroyView.as_view(), name='retrive_update_delete'),
]
