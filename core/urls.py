from django.urls import path
from .views import *

urlpatterns = [
    path('places/', PlaceListView.as_view()),
    path('places/<pk>/', PlaceDetailView.as_view()),

    path('categories/', CategoryListView.as_view()),
    path('categories/<pk>/', CategoryDetailView.as_view()),

    path('menu_items/', MenuItemListView.as_view()),
    path('menu_items/<pk>', MenuItemDetailView.as_view()),

    path('create_payment_intent/', create_payment_intent),

    path('orders/', OrderListView.as_view()),
    path('orders/<pk>', OrderDetailView.as_view()),
]