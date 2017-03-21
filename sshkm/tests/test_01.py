import time
from django.test import TestCase, Client, override_settings
from sshkm.models import Host, Group, Key, Osuser, Permission

class Test01(TestCase):
    fixtures = ['sshkm/tests/fixtures/testdata.json']

    def setUp(self):
        self.username = "admin"
        self.password = "admin"

        self.client.post('/login/', {'username': self.username, 'password': self.password})

    def test_group_new(self):
        response = self.client.post('/group/save/', {'name': 'testgroup1', 'description': 'testgroup1 description'})
        self.assertEqual(Group.objects.get(name='testgroup1').description, "testgroup1 description")

    def test_key(self):
        response = self.client.post('/key/save/', {'name': 'testkey2', 'description': 'testkey2 description'})
        self.assertEqual(Key.objects.get(name='testkey2').description, "testkey2 description")
        response = self.client.get('/key/delete/', {'id': Key.objects.get(name='testkey2').id}, follow=True)
        self.assertEqual(Key.objects.filter(name='testkey2').count(), 0)

    def test_osuser_new(self):
        response = self.client.post('/osuser/save/', {'name': 'testosuser1', 'description': 'testosuser1 description'})
        self.assertEqual(Osuser.objects.get(name='testosuser1').description, "testosuser1 description")

    #def test_permission_new(self):
    #    response = self.client.post('/group/save/', {'name': 'testgroup1', 'description': 'testgroup1 description', 'members': []})
    #    self.assertEqual(Group.objects.get(name='testgroup1').description, "testgroup1 description")

    def test_host_new(self):
        response = self.client.post('/host/save/', {'name': 'testhost1', 'description': 'testhost1 description'})
        self.assertEqual(Host.objects.get(name='testhost1').description, "testhost1 description")

    def test_host_deploy_single(self):
        response = self.client.get('/host/deploy/', {'id': 1}, follow=True)
        self.assertContains(response, 'deployed', status_code=200)
        self.assertEqual(Host.objects.get(id=1).status, "SUCCESS")

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, BROKER_BACKEND='memory')
    def test_host_deploy_multiple(self):
        response = self.client.post('/host/deploy/', {'id_multiple': [1]}, follow=True)
        self.assertContains(response, 'Multiple host deployment initiated', status_code=200)
        time.sleep(10)
        response = self.client.get('/host/', follow=True)
        self.assertEqual(Host.objects.get(id=1).status, "SUCCESS")

