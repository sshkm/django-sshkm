from django.test import TestCase, Client

class TestDocs(TestCase):
    def setUp(self):
        pass

    def test_docs_main_content(self):
        #c = Client()
        #csrf_client = Client(enforce_csrf_checks=True)
        #response = self.client.get("/path/to/resource/pk/")
        #response = self.client.post('/group/', {'username': 'admin', 'password': 'admin'})
        response = self.client.get('/docs/')
        self.assertContains(response, '<h1>Documentation</h1>', status_code=200)
        #self.assertTemplateUsed(response, 'group/list.html')
