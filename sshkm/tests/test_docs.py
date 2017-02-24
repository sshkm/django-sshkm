from django.test import TestCase, Client

class TestDocs(TestCase):
    def setUp(self):
        pass

    def test_docs_main_content(self):
        response = self.client.get('/docs/')
        self.assertContains(response, '<h1>Documentation</h1>', status_code=200)
