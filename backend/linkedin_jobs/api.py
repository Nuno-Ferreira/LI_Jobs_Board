from urllib.parse import urlencode
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LinkedinAuth, LinkedinJob
from .serializers import LinkedinJobSerializer

class LinkedinJobListCreateAPI(APIView):
    def get(self, request):
        jobs = LinkedinJob.objects.all()
        serializer = LinkedinJobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LinkedinJobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinkedinAuthURL(APIView):
    def get(self, request):
        state = str(uuid.uuid4()) # Generate a random string to prevent CSRF attacks

        # Save the state to the database to verify it later
        auth = LinkedinAuth(state=state)
        auth.save()

        # Build the Auth URL params
        params = {
            "response_type": "code",
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "state": state,
            "scope": settings.LINKEDIN_SCOPE,
        }

        # Build the Auth URL
        auth_url = f"{settings.LINKEDIN_AUTH_URL}?{urlencode(params)}"

        return Response({
            "auth_url": auth_url,
            "state": state,
        })


class LinkedinCallback(APIView):
    def get(self, request):
        # Extract the "code" and "state" from the query parameters
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code or not state:
            return Response({"error": "Missing code or state parameter"}, status=400)

        # Validate the state
        try:
            get_object_or_404(LinkedinAuth, state=state)
        except LinkedinAuth.DoesNotExist:
            return Response({"error": "Invalid state parameter"}, status=400)

        # Exchange the authorization code for an access token
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        }

        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_response = response.json()
        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to fetch access token", "details": str(e)}, status=500)

        # Return the access token
        return Response({
            "access_token": token_response.get("access_token"),
            "expires_in": token_response.get("expires_in"),
        })
