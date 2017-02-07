#from django.utils.translation import ugettext_lazy as _
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
