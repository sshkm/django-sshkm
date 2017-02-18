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
            'member_of': _('Member of Group(s)'),
        }

    def __init__(self, *args, **kwargs):
        super(KeyForm, self).__init__(*args, **kwargs)
        self.fields['member_of'] = ModelMultipleChoiceFieldNames(queryset=Group.objects.all(), required=False)
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['description'].widget.attrs['placeholder'] = ''
        self.fields['publickey'].widget.attrs['placeholder'] = 'ssh-rsa AAAAB3NzaC1yc......== user@example.com'

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description', 'members',)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['members'] = ModelMultipleChoiceFieldNames(queryset=Key.objects.all(), required=False)

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ('name', 'description',)

class OsuserForm(forms.ModelForm):
    class Meta:
        model = Osuser
        fields = ('name', 'home', 'description',)

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('host', 'group', 'osuser',)

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['host'] = ModelMultipleChoiceFieldNames(queryset=Host.objects.all())
        self.fields['group'] = ModelMultipleChoiceFieldNames(queryset=Group.objects.all())
        self.fields['osuser'] = ModelMultipleChoiceFieldNames(queryset=Osuser.objects.all())

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('password',)

