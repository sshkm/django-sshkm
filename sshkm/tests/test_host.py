from django.test import TestCase, Client
from sshkm.models import Host

class TestHost(TestCase):
    fixtures = ['sshkm/tests/fixtures/testdata.json']

    def setUp(self):
        self.username = "admin"
        self.password = "admin"

        self.client.post('/login/', {'username': self.username, 'password': self.password})

    def test_host_deploy_single(self):
        pass
        #response = self.client.get('/host/deploy/', {'id': 1}, follow=True)
        #self.assertContains(response, 'deployed', status_code=200)
        #self.assertEqual(Host.objects.get(id=1).status, "SUCCESS")
