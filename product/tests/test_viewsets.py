from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.factories import CategoryFactory, ProductFactory
from product.models import Category, Product


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory(title="Romance", slug="romance")

    def test_lista_categorias(self):
        response = self.client.get(reverse("category-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["title"], "Romance")

    def test_cria_categoria(self):
        response = self.client.post(reverse("category-list"), {"title": "Terror", "slug": "terror"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(slug="terror").exists())

    def test_cria_categoria_invalida(self):
        response = self.client.post(reverse("category-list"), {"title": "Sem slug"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detalhe_e_remocao(self):
        url = reverse("category-detail", args=[self.category.id])

        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.exists())


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory(title="Tecnologia", slug="tecnologia")
        self.product = ProductFactory(title="Python Fluente", price=120, category=[self.category])

    def test_lista_produtos_com_categoria(self):
        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = response.json()[0]
        self.assertEqual(product["title"], "Python Fluente")
        self.assertEqual(product["category"][0]["slug"], "tecnologia")

    def test_cria_produto(self):
        data = {"title": "Django na prática", "price": 89, "categories_id": [self.category.id]}

        response = self.client.post(reverse("product-list"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Product.objects.get(title="Django na prática")
        self.assertEqual(list(created.category.all()), [self.category])

    def test_atualiza_preco(self):
        url = reverse("product-detail", args=[self.product.id])

        response = self.client.patch(url, {"price": 99}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 99)

    def test_remove_produto(self):
        response = self.client.delete(reverse("product-detail", args=[self.product.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.exists())
