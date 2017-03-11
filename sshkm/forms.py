from django import forms
from .models import Key, Group, Host, Osuser, KeyGroup, Permission
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelMultipleChoiceField


# return names of object in MultipleChoiceField
class ModelMultipleChoiceFieldNames(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name
 

class KeyForm(forms.ModelForm):
    class Meta:
        model = Key
        fields = ('name', 'email', 'description', 'firstname', 'lastname', 'publickey', 'member_of',)
        labels = {
            'name': _('Name (unique)'),
            'email': _('Email (optional)'),
            'description': _('Description (optional)'),
            'firstname': _('Firstname (optional)'),
            'lastname': _('Lastname (optional)'),
            'publickey': _('Public Key'),
        }

    def __init__(self, *args, **kwargs):
        super(KeyForm, self).__init__(*args, **kwargs)
        self.fields['member_of'] = ModelMultipleChoiceFieldNames(queryset=Group.objects.all(), required=False, label='Member of Group(s)')
        self.fields['name'].widget.attrs['placeholder'] = ''
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['firstname'].widget.attrs['placeholder'] = ''
        self.fields['lastname'].widget.attrs['placeholder'] = ''
        self.fields['description'].widget.attrs['placeholder'] = ''
        self.fields['publickey'].widget.attrs['placeholder'] = 'ssh-rsa AAAAB3NzaC1yc......== user@example.com'

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description', 'members',)
        labels = {
            'name': _('Groupname (department, external company, remote hostgroup, ...)'),
            'description': _('Description (optional)'),
        }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['members'] = ModelMultipleChoiceFieldNames(queryset=Key.objects.all(), required=False, label='Members (Key(s))')
        self.fields['name'].widget.attrs['placeholder'] = ''
        self.fields['description'].widget.attrs['placeholder'] = ''

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ('name', 'superuser', 'description',)
        labels = {
            'name': _('Host or IP'),
            'superuser': _('Superuser'),
            'description': _('Description (optional)'),
        }

    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'host1.example.com or 192.168.1.33'
        self.fields['superuser'].widget.attrs['placeholder'] = 'default: root'
        self.fields['superuser'].label = 'Superuser (OS-User used to connect to your host to deploy all other keys)'
        self.fields['description'].widget.attrs['placeholder'] = ''

class OsuserForm(forms.ModelForm):
    class Meta:
        model = Osuser
        fields = ('name', 'home', 'description',)
        labels = {
            'name': _('Username'),
            'home': _('Home Directory (optional)'),
            'description': _('Description (optional)'),
        }

    def __init__(self, *args, **kwargs):
        super(OsuserForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'root, oracle, john, ...'
        self.fields['home'].widget.attrs['placeholder'] = '/root, /home/oracle, ...'
        self.fields['description'].widget.attrs['placeholder'] = ''

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('host', 'group', 'osuser',)

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['host'] = ModelMultipleChoiceFieldNames(queryset=Host.objects.all().order_by('name'), label='Select host(s) on which you want to set perssion(s):')
        self.fields['group'] = ModelMultipleChoiceFieldNames(queryset=Group.objects.all().order_by('name'), label='Select the group(s) which has/have permission on the selected host(s):')
        self.fields['osuser'] = ModelMultipleChoiceFieldNames(queryset=Osuser.objects.all().order_by('name'), label='Select OS-User(s) on which the key(s) in the selected group(s) should be allowed to connect on the selected hosts(s):')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('password',)

