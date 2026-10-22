from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Exam, Question, Option
from .serializers import ExamSerializer, QuestionSerializer, OptionSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all().order_by('-created_at')
    serializer_class = ExamSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('id')
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['exam']
    search_fields = ['text']


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all().order_by('id')
    serializer_class = OptionSerializer
