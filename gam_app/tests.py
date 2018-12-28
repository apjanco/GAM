from django.test import TestCase


class TestPages(TestCase):
    """Test that the proper templates are used to render pages.

    This test suite will catch the following errors for the URLs that it tests:
      - The URL does not exist (HTTP 404).
      - The view function throws an exception.
      - The wrong template is used to render the page.
    """

    def test_index_page(self):
        response = self.client.get('/en/')
        self.assertTemplateUsed(response, 'index.html')
