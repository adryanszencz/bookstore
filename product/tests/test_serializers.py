from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.models import Product
from product.serializers import CategorySerializer, ProductSerializer


class CategorySerializerTest(TestCase):
    def test_retorna_os_campos_esperados(self):
        category = CategoryFactory(title="Romance", slug="romance")

        data = CategorySerializer(category).data

        self.assertEqual(set(data), {"id", "title", "slug", "description", "active"})
        self.assertEqual(data["title"], "Romance")

    def test_dados_validos_sao_aceitos(self):
        serializer = CategorySerializer(data={"title": "Ficção", "slug": "ficcao"})

        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()
        self.assertTrue(category.active)

    def test_titulo_e_slug_sao_obrigatorios(self):
        serializer = CategorySerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("slug", serializer.errors)

    def test_slug_invalido_e_rejeitado(self):
        serializer = CategorySerializer(data={"title": "Terror", "slug": "com espaço!"})

        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)

    def test_slug_repetido_e_rejeitado(self):
        CategoryFactory(slug="terror")

        serializer = CategorySerializer(data={"title": "Terror", "slug": "terror"})

        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = CategoryFactory(title="Tecnologia", slug="tecnologia")

    def test_retorna_os_campos_esperados(self):
        product = ProductFactory(category=[self.category])

        data = ProductSerializer(product).data

        self.assertEqual(set(data), {"id", "title", "description", "price", "active", "category"})

    def test_categoria_aparece_dentro_do_produto(self):
        product = ProductFactory(title="Python Fluente", category=[self.category])

        data = ProductSerializer(product).data

        self.assertEqual(len(data["category"]), 1)
        self.assertEqual(data["category"][0]["title"], "Tecnologia")
        self.assertEqual(data["category"][0]["slug"], "tecnologia")

    def test_cria_produto_com_categorias(self):
        serializer = ProductSerializer(
            data={"title": "Django na prática", "price": 89, "categories_id": [self.category.id]}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(list(product.category.all()), [self.category])

    def test_titulo_e_obrigatorio(self):
        serializer = ProductSerializer(data={"price": 10})

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_preco_negativo_e_rejeitado(self):
        serializer = ProductSerializer(data={"title": "Livro", "price": -5})

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_categoria_inexistente_e_rejeitada(self):
        serializer = ProductSerializer(data={"title": "Livro", "price": 10, "categories_id": [999]})

        self.assertFalse(serializer.is_valid())
        self.assertIn("categories_id", serializer.errors)
