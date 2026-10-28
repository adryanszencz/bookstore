from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(title="Dom Casmurro", price=30)
        self.order = OrderFactory(user=self.user, product=[self.product])

    def test_lista_pedidos(self):
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = response.json()["results"][0]
        self.assertEqual(order["product"][0]["title"], "Dom Casmurro")
        self.assertEqual(order["total"], 30)

    def test_cria_pedido(self):
        other = ProductFactory(price=20)
        data = {"user": self.user.id, "products_id": [self.product.id, other.id]}

        response = self.client.post(reverse("order-list"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["total"], 50)
        self.assertEqual(Order.objects.count(), 2)

    def test_pedido_sem_produto_da_400(self):
        response = self.client.post(reverse("order-list"), {"user": self.user.id, "products_id": []}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detalhe_e_remocao(self):
        url = reverse("order-detail", args=[self.order.id])

        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.exists())
