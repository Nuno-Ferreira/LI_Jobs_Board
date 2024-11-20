from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LinkedinJob
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
