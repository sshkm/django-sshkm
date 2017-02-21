from django.test import TestCase, Client

class TestHost(TestCase):
    def setUp(self):
        pass

    def test_host_deploy_single(self):
        #c = Client()
        #csrf_client = Client(enforce_csrf_checks=True)
        #response = self.client.get("/path/to/resource/pk/")
        response = self.client.post('/group/', {'username': 'admin', 'password': 'admin'})
        response = self.client.get('/host/deploy/?id=1')
        #self.assertContains(response, '<h1>Documentation</h1>', status_code=200)
        #self.assertTemplateUsed(response, 'group/list.html')
