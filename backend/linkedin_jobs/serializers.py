from rest_framework import serializers
from .models import LinkedinJob

class LinkedinJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedinJob
        fields = '__all__'
