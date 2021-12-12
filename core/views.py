from rest_framework import generics
from . import models, serializers, permissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import stripe
import sys




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
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.CategorySerializer


class CategoryDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class MenuItemListView(generics.CreateAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.MenuItemSerializer


class MenuItemDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.all()


class OrderListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return models.Order.objects.filter(
            place__owner_id=self.request.user.id, 
            place_id=self.request.GET.get('place'))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class OrderDetailView(generics.UpdateAPIView):
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()


stripe.api_key = settings.STRIPE_API_SECRET_KEY

@csrf_exempt
def create_payment_intent(request):
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode) 
        intent = stripe.PaymentIntent.create(
            amount = data['amount'] *  100,
            currency = 'usd',
            payment_method = data['payment_method']['id'],
            off_session = True,
            confirm = True
        )
        order = models.Order.objects.create(
            place_id = data['place'],
            table = data['table'],
            detail = json.dumps(data['detail']),
            amount = data['amount'],
            payment_intent = intent['id']
        )

        return JsonResponse({
            "success": True,
            'order': order.id
        })
    except Exception as e:

        return JsonResponse({
            "success": False,
            'error': str(e)
        })