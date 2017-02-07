from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^help/$', views.help, name='help'),
    #url(r'^host/deploy/$', views.HostDeploy, name='HostDeploy'),

    url(r'^key/$', views.KeyList, name='KeyList'),
    url(r'^key/detail/$', views.KeyDetail, name='KeyDetail'),
    url(r'^key/delete/$', views.KeyDelete, name='KeyDelete'),
    url(r'^key/save/$', views.KeySave, name='KeySave'),
    url(r'^key/task_state/$', views.task_state, name='task_state'),

    url(r'^group/$', views.GroupList, name='GroupList'),
    url(r'^group/detail/$', views.GroupDetail, name='GroupDetail'),
    url(r'^group/delete/$', views.GroupDelete, name='GroupDelete'),
    url(r'^group/save/$', views.GroupSave, name='GroupSave'),

    url(r'^host/$', views.HostList, name='HostList'),
    url(r'^host/detail/$', views.HostDetail, name='HostDetail'),
    url(r'^host/delete/$', views.HostDelete, name='HostDelete'),
    url(r'^host/save/$', views.HostSave, name='HostSave'),
    url(r'^host/deploy/$', views.HostDeploy, name='HostDeploy'),

    url(r'^osuser/$', views.OsuserList, name='OsuserList'),
    url(r'^osuser/detail/$', views.OsuserDetail, name='OsuserDetail'),
    url(r'^osuser/delete/$', views.OsuserDelete, name='OsuserDelete'),
    url(r'^osuser/save/$', views.OsuserSave, name='OsuserSave'),

    url(r'^permission/$', views.PermissionList, name='PermissionList'),
    url(r'^permission/create/$', views.PermissionCreate, name='PermissionCreate'),
    url(r'^permission/delete/$', views.PermissionDelete, name='PermissionDelete'),
    url(r'^permission/save/$', views.PermissionSave, name='PermissionSave'),

    url(r'^settings/$', views.SettingsList, name='SettingsList'),
    #url(r'^settings/passwordreset/$', views.PasswordReset, name='PasswordReset'),
    url(r'^settings/passwordsave/$', views.PasswordSave, name='PasswordSave'),
    url(r'^settings/createuser/$', views.CreateUser, name='CreateUser'),
    url(r'^settings/deleteuser/$', views.DeleteUser, name='DeleteUser'),

    #url(r'^permission/$', views.PermissionList, name='PermissionList'),
    #url(r'^(?P<network_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^create_network/$', views.create_network, name='create_network'),
    #url(r'^create_host/$', views.create_host, name='create_host'),
    #url(r'^delete_network/$', views.delete_network, name='delete_network'),
    #url(r'^delete_host/$', views.delete_host, name='delete_host'),
]
