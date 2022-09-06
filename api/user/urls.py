from django.urls import path
from .apis import UserAPI

urlpatterns = [
    path('registration', UserAPI.as_view({'post': 'registration'}), name='user_registration'),
    path('verify-registration', UserAPI.as_view({'post': 'registration_verification'}), name='registration_verification'),
    path('authentication', UserAPI.as_view({'post': 'authentication'}), name='authentication'),
    path('verify-authentication', UserAPI.as_view({'post': 'authentication_verification'}), name='authentication_verification')
]
