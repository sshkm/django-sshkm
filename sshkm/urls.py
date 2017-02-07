### for initial setup
from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS
from django.core.management import call_command

connection = connections[DEFAULT_DB_ALIAS]
connection.prepare_database()
executor = MigrationExecutor(connection)
targets = executor.loader.graph.leaf_nodes()

if executor.migration_plan(targets):
    executor.migrate(targets)
    call_command('loaddata', 'setup')
###

from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('keymaster.urls')),
    url(r'^keymaster/', include('keymaster.urls')),
    url(r'^authentication/', include('authentication.urls')),
]
