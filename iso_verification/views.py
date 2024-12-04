from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .models import Question, UserResponse, Option
from django.contrib.auth import logout # type: ignore
from .forms import QuestionForm
from django.contrib import messages
from django.dispatch import receiver


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def quiz_view(request):
    user = request.user
    #imprimir ifnormacion del usuario
    print(user)
    # Obtener preguntas no respondidas por el usuario
    unanswered_questions = Question.objects.exclude(
        id__in=UserResponse.objects.filter(user=user).values('question')
    ).order_by('id')

    # Calcular progreso
    total_questions = Question.objects.count()
    answered_questions = total_questions - unanswered_questions.count()
    progress = int((answered_questions / total_questions) * 100) if total_questions > 0 else 0

    # Si no hay más preguntas por responder, redirigir a la página de finalización
    if not unanswered_questions.exists():
        return redirect('quiz_complete')

    # Obtener la siguiente pregunta no respondida
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = QuestionForm(request.POST, question=question)  # Crear el formulario con la pregunta actual

        if form.is_valid():
            selected_option_id = form.cleaned_data['selected_option']
            try:
                selected_option = Option.objects.get(id=selected_option_id)

                # Crear la respuesta del usuario
                UserResponse.objects.create(
                    user=user,
                    question=question,
                    selected_option=selected_option
                )

                # Redirigir a la misma vista para continuar con la siguiente pregunta
                return redirect('quiz')

            except Option.DoesNotExist:
                pass
    else:
        form = QuestionForm(question=question)  # Crear el formulario cuando la solicitud no es POST

    # Contexto para renderizar la plantilla
    context = {
        'form': form,
        'progress': progress,
        'question': question,  # Agregar la pregunta actual al contexto
    }

    return render(request, 'quiz.html', context)


from collections import Counter

@login_required
def quiz_complete(request):
    user = request.user

    # Obtener las respuestas del usuario
    responses = UserResponse.objects.filter(user=user).select_related('question__classification', 'selected_option')

    # Agrupar respuestas por clasificación y contar cada tipo de respuesta
    grouped_responses = {}
    classification_counts = {}
    for response in responses:
        classification = response.question.classification
        if classification not in grouped_responses:
            grouped_responses[classification] = {
                'si': [],
                'no': [],
                'parcialmente': [],
            }
            classification_counts[classification] = Counter({'si': 0, 'no': 0, 'parcialmente': 0})

        # Clasificar respuestas según la opción seleccionada
        option = response.selected_option.text.lower()
        grouped_responses[classification][option].append(response)
        classification_counts[classification][option] += 1

    context = {
        'grouped_responses': grouped_responses,
        'classification_counts': classification_counts,
    }

    return render(request, 'quiz_complete.html', context)
