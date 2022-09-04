from django.urls import path
from .apis import UserAPI

urlpatterns = [
    path('registration', UserAPI.as_view({'post': 'registration'}), name='user_registration')
]
