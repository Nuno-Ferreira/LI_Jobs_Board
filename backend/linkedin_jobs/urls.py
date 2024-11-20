from django.urls import path
from .api import LinkedinJobListCreateAPI

urlpatterns = [
    path('jobs/', LinkedinJobListCreateAPI.as_view(), name='jobs')
]
