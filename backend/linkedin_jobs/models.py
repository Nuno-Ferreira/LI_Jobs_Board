from django.db import models

class LinkedinJob(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
