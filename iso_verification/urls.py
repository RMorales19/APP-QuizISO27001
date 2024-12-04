from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from iso_verification.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('accounts/quiz/', login_required(quiz_view), name='quiz'),
    path('accounts/quiz/results/', login_required(quiz_complete), name='quiz_complete'),
    path('', RedirectView.as_view(pattern_name='quiz', permanent=False)),
]
