import time
from django.test import TestCase, Client, override_settings
from sshkm.models import Host

class TestHost(TestCase):
    fixtures = ['sshkm/tests/fixtures/testdata.json']

    def setUp(self):
        self.username = "admin"
        self.password = "admin"

        self.client.post('/login/', {'username': self.username, 'password': self.password})

    def test_host_deploy_single(self):
        response = self.client.get('/host/deploy/', {'id': 1}, follow=True)
        self.assertContains(response, 'deployed', status_code=200)
        self.assertEqual(Host.objects.get(id=1).status, "SUCCESS")

#    #@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
#    def test_host_deploy_multiple(self):
#        response = self.client.post('/host/deploy/', {'id_multiple': [1]}, follow=True)
#        self.assertContains(response, 'Multiple host deployment initiated', status_code=200)
#        time.sleep(5)
#        response = self.client.get('/host/', follow=True)
#        print(str(response))
#        time.sleep(5)
#        self.assertEqual(Host.objects.get(id=1).status, "SUCCESS")
