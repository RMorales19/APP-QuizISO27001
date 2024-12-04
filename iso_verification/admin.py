from django.contrib import admin
from .models import Classification, Question, Option, UserResponse

# Registrar los modelos
admin.site.register(Classification)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserResponse)
