from django.urls import path
from .views import ContractListCreateView, ContractRetrieveUpdateDestroyView

urlpatterns = [
    path('', ContractListCreateView.as_view(), name='contract-list-create'),
    path('<int:pk>/', ContractRetrieveUpdateDestroyView.as_view(), name='contract-detail'),
]