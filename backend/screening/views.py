from django.shortcuts import render
import os
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer
from .ai_module import analyze_resume

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all().order_by('-upload_date')
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume_instance = serializer.save()
        
        # Compute the AI score using the uploaded file's path
        score = analyze_resume(resume_instance.resume_file.path, analysis_type="score")
        review = analyze_resume(resume_instance.resume_file.path, analysis_type="review")
        resume_instance.score = score
        resume_instance.review = review
        resume_instance.save()
        os.remove(resume_instance.resume_file.path)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
