from django.urls import path
from .views import BinnacleView

urlpatterns = [
    path('',BinnacleView.as_view(),name='binn'),
]
