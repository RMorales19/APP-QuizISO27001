from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore


class Classification(models.Model):
    """Modelo para clasificaciones de preguntas."""
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'classification'

    def __str__(self):
        return self.name
    

class Question(models.Model):
    """Modelo para las preguntas."""
    topic = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    classification = models.ForeignKey(Classification, related_name='questions', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'question'
    def __str__(self):
        return self.text


class Option(models.Model):
    """Las opciones son: Si, No, Parcialmente"""
    text = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'option'
    def __str__(self):
        return self.text


class UserResponse(models.Model):
    """Modelo para guardar las respuestas de los usuarios."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    selected_option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('user', 'question')
        db_table = 'user_response'

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"
