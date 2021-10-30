from rest_framework import generics
from . import models, serializers, permissions


class PlaceListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.PlaceSerializer

    def get_queryset(self):
        return models.Place.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.PlaceOwnerOrReadOnly]
    serializer_class = serializers.PlaceDetailSerializer
    queryset = models.Place.objects.all()

class CategoryListView(generics.CreateAPIView):
    permission_classes = [permissions.PlaceOwnerOrReadOnly]
    serializer_class = serializers.CategorySerializer


class CategoryDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.PlaceOwnerOrReadOnly]
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class MenuItemListView(generics.CreateAPIView):
    permission_classes = [permissions.PlaceOwnerOrReadOnly]
    serializer_class = serializers.MenuItemSerializer


class MenuItemDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.PlaceOwnerOrReadOnly]
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.all()
