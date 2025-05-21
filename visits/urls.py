from django.urls import path
from .views import VisitListCreateView, VisitRetrieveUpdateDestroyView

urlpatterns = [
    path('', VisitListCreateView.as_view(), name='visit-list-create'),
    path('<int:pk>/', VisitRetrieveUpdateDestroyView.as_view(), name='visit-detail'),
]