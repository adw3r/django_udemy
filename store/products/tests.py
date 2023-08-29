from http import HTTPStatus

from django.test import testcases
from django.urls import reverse
from products.models import Product, ProductCategory


class IndexViewTestCase(testcases.TestCase):

    def test_view(self):
        path: str = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Django store')

        self.assertTemplateUsed(response, 'products/base.html')
        self.assertTemplateUsed(response, 'products/index.html')

        print(response)


class ProductListViewTestCase(testcases.TestCase):
    fixtures = [
        'categories.json',
        'products.json'
    ]

    def setUp(self) -> None:
        self.products = Product.objects.all()

    def test_view(self):
        path: str = reverse('products:index')
        response = self.client.get(path)
        print(response)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_category(self):
        category = ProductCategory.objects.first()
        path: str = reverse('products:category', args=(category.id,))
        response = self.client.get(path)
        print(response)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']), list(self.products.filter(category_id=category.id)[:3])
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/base.html')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'My products')
