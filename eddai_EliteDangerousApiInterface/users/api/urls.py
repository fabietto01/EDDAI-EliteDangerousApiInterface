from django.urls import path
from .venws import UserSessionView, UserProfileView

urlpatterns = [
    path('session', UserSessionView.as_view(), name='user-session'),
    path('profile', UserProfileView.as_view(), name='user-profile'),
]
