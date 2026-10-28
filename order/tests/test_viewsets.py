from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.product = ProductFactory(title="Dom Casmurro", price=30)
        self.order = OrderFactory(user=self.user, product=[self.product])

    def test_sem_token_da_401(self):
        self.client.credentials()

        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_invalido_da_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalido")

        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lista_pedidos(self):
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = response.json()["results"][0]
        self.assertEqual(order["product"][0]["title"], "Dom Casmurro")
        self.assertEqual(order["total"], 30)

    def test_usuario_so_ve_os_proprios_pedidos(self):
        OrderFactory(user=UserFactory(), product=[self.product])

        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.json()["count"], 1)

    def test_pedido_de_outro_usuario_da_404(self):
        other_order = OrderFactory(user=UserFactory(), product=[self.product])

        response = self.client.get(reverse("order-detail", args=[other_order.id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cria_pedido_com_o_usuario_do_token(self):
        other = ProductFactory(price=20)

        response = self.client.post(
            reverse("order-list"), {"products_id": [self.product.id, other.id]}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["total"], 50)
        self.assertEqual(response.json()["user"], self.user.id)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 2)

    def test_pedido_sem_produto_da_400(self):
        response = self.client.post(reverse("order-list"), {"products_id": []}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detalhe_e_remocao(self):
        url = reverse("order-detail", args=[self.order.id])

        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.exists())


class ProductContinuaAbertoTest(APITestCase):
    def test_produtos_nao_exigem_token(self):
        ProductFactory()

        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ObtainTokenTest(APITestCase):
    def test_gera_token_com_usuario_e_senha(self):
        user = UserFactory()
        user.set_password("senha-de-teste-123")
        user.save()

        response = self.client.post(
            reverse("api_token_auth"),
            {"username": user.username, "password": "senha-de-teste-123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["token"], Token.objects.get(user=user).key)
