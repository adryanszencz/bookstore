from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.factories import ProductFactory


class PaginationTest(APITestCase):
    def setUp(self):
        ProductFactory.create_batch(12)

    def test_primeira_pagina_tem_5_produtos(self):
        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 12)
        self.assertEqual(len(body["results"]), 5)
        self.assertIsNotNone(body["next"])
        self.assertIsNone(body["previous"])

    def test_ultima_pagina(self):
        response = self.client.get(reverse("product-list"), {"page": 3})

        body = response.json()
        self.assertEqual(len(body["results"]), 2)
        self.assertIsNone(body["next"])

    def test_pagina_inexistente_da_404(self):
        response = self.client.get(reverse("product-list"), {"page": 10})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
