from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    """Pedidos exigem login (token): cada usuário só vê e cria os próprios pedidos."""

    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("product__category")
            .order_by("id")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
