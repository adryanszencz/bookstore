from django.test import TestCase

from order.factories import OrderFactory, UserFactory
from order.serializers import OrderSerializer
from product.factories import CategoryFactory, ProductFactory


class OrderSerializerTest(TestCase):
    def setUp(self):
        category = CategoryFactory(title="Infantil", slug="infantil")
        self.product_1 = ProductFactory(title="O Pequeno Príncipe", price=40, category=[category])
        self.product_2 = ProductFactory(title="Alice", price=35)
        self.user = UserFactory()

    def test_retorna_os_campos_esperados(self):
        order = OrderFactory(user=self.user, product=[self.product_1])

        data = OrderSerializer(order).data

        self.assertEqual(set(data), {"id", "product", "user", "total"})

    def test_produtos_aparecem_com_as_categorias(self):
        order = OrderFactory(user=self.user, product=[self.product_1])

        data = OrderSerializer(order).data

        self.assertEqual(data["product"][0]["title"], "O Pequeno Príncipe")
        self.assertEqual(data["product"][0]["category"][0]["slug"], "infantil")

    def test_total_soma_os_precos(self):
        order = OrderFactory(user=self.user, product=[self.product_1, self.product_2])

        self.assertEqual(OrderSerializer(order).data["total"], 75)

    def test_cria_pedido(self):
        serializer = OrderSerializer(
            data={"user": self.user.id, "products_id": [self.product_1.id, self.product_2.id]}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.product.count(), 2)
        self.assertEqual(order.user, self.user)

    def test_usuario_e_produtos_sao_obrigatorios(self):
        serializer = OrderSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
        self.assertIn("products_id", serializer.errors)

    def test_pedido_sem_produto_e_rejeitado(self):
        serializer = OrderSerializer(data={"user": self.user.id, "products_id": []})

        self.assertFalse(serializer.is_valid())
        self.assertIn("products_id", serializer.errors)

    def test_produto_inexistente_e_rejeitado(self):
        serializer = OrderSerializer(data={"user": self.user.id, "products_id": [999]})

        self.assertFalse(serializer.is_valid())
        self.assertIn("products_id", serializer.errors)
