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
    path('logout/', logout_all_users, name='logout'),
    
    path('accounts/quiz/', login_required(TemplateView.as_view(template_name='quiz.html')), name='quiz'),
    path('', RedirectView.as_view(pattern_name='quiz', permanent=False)),
]
