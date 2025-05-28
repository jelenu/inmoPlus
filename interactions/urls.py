from django.urls import path
from .views import FavoriteViewSet, ContactFormCreateView

favorite_list = FavoriteViewSet.as_view({'get': 'list'})
favorite_toggle = FavoriteViewSet.as_view({'post': 'toggle'})

urlpatterns = [
    path('favorites/', favorite_list, name='favorite-list'),
    path('favorites/<int:pk>/toggle/', favorite_toggle, name='favorite-toggle'),
    path('contact/', ContactFormCreateView.as_view(), name='contact-form-create'),
]
