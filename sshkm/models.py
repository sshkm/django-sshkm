from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100)
    base_url = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu)
    order = models.IntegerField(default=500)
    link_url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    login_required = models.BooleanField(blank=True, default=False)
    staff_required = models.BooleanField(blank=True, default=False)
    anonymous_only = models.BooleanField(blank=True, default=False)

class Group(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    members = models.ManyToManyField('Key', through='KeyGroup', blank=True)
    #members = models.ManyToManyField('Key')

class Host(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    task_id = models.CharField(max_length=36, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)

class Osuser(models.Model):
    name = models.CharField(max_length=200, unique=True)
    home = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

KEYTYPE_CHOICES = (
    ('ssh-rsa', 'ssh-rsa'),
    ('ssh-dsa', 'ssh-dsa'),
)

class Key(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    keytype = models.CharField(max_length=10, null=True, choices=KEYTYPE_CHOICES, default='RSA',)
    publickey = models.TextField(null=True, blank=True)
    member_of = models.ManyToManyField('Group', through='KeyGroup', blank=True)
    #member_of = models.ManyToManyField('Group')
#    def __str__(self):
#        return self.name
#    def __unicode__(self):
#        return self.name

class KeyGroup(models.Model):
    key = models.ForeignKey('Key', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

class Permission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    osuser = models.ForeignKey(Osuser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("group", "host", "osuser")
