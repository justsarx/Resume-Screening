from django.db import models

# Create your models here.
from django.db import models

class Resume(models.Model):
    candidate_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    resume_file = models.FileField(upload_to='resumes/')
    upload_date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)  # AI ranking score
    review = models.TextField(null=True, blank=True) # AI review

    def __str__(self):
        return self.candidate_name
