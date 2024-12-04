from django.db import models
from django.contrib.auth.models import User


class Classification(models.Model):
    """Modelo para clasificaciones de preguntas."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subclassification(models.Model):
    """Modelo para subclasificaciones de preguntas."""
    classification = models.ForeignKey(Classification, related_name='subclassifications', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.classification.name} - {self.name}"


class Question(models.Model):
    """Modelo para las preguntas."""
    text = models.CharField(max_length=255)
    subclassification = models.ForeignKey(Subclassification, related_name='questions', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text


class Option(models.Model):
    """Modelo para las opciones de respuesta que son iguales para todas las preguntas."""
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)  # Esto puede no ser necesario si no se usan respuestas correctas.
    
    def __str__(self):
        return self.text


class UserResponse(models.Model):
    """Modelo para guardar las respuestas de los usuarios."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    google_user_id = models.CharField(max_length=255, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    selected_option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"

