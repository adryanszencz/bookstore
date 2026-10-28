import factory

from product.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: f"Categoria {n}")
    slug = factory.Sequence(lambda n: f"categoria-{n}")
    description = factory.Faker("sentence", locale="pt_BR")
    active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    title = factory.Sequence(lambda n: f"Livro {n}")
    description = factory.Faker("sentence", locale="pt_BR")
    price = factory.Faker("pyint", min_value=10, max_value=200)
    active = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if create and extracted:
            self.category.set(extracted)
