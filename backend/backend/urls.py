from django.urls import path
from .views import run_hackrx

urlpatterns = [
    path('hackrx/run', run_hackrx),
]
