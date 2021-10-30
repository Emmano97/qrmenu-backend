from django.urls import path
from .views import *

urlpatterns = [
    path('places/', PlaceListView.as_view()),
    path('places/<pk>', PlaceDetailView.as_view()),

    path('categories/', CategoryListView.as_view()),
    path('categories/<pk>', CategoryDetailView.as_view()),

    path('munu_items/', MenuItemListView.as_view()),
    path('munu_items/<pk>', MenuItemDetailView.as_view()),
]