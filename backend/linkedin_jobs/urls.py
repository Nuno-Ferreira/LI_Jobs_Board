from django.urls import path
from .api import LinkedinJobListCreateAPI, LinkedinAuthURL, LinkedinCallback

urlpatterns = [
    path('jobs/', LinkedinJobListCreateAPI.as_view(), name='jobs'),
    path('auth/linkedin/', LinkedinAuthURL.as_view(), name='linkedin_auth_url'),
    path('auth/linkedin/callback/', LinkedinCallback.as_view(), name='linkedin_callback'),
]
