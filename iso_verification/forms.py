from django import forms
from .models import Option

class QuestionForm(forms.Form):
    """Formulario para seleccionar una respuesta para una pregunta."""

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')  # Se pasa la pregunta como argumento
        super().__init__(*args, **kwargs)

        # Cargar todas las opciones disponibles
        choices = [(option.id, option.text) for option in Option.objects.all()]

        # Campo para seleccionar una opción
        self.fields['selected_option'] = forms.ChoiceField(
            choices=choices,
            widget=forms.RadioSelect(attrs={'class': 'option-input'}),
            required=True,
            label=question.text
        )
