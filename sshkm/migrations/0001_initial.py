# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 09:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                #('task_id', models.CharField(blank=True, max_length=36, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('publickey', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sshkm.Group')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sshkm.Key')),
            ],
        ),
        migrations.CreateModel(
            name='Osuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('home', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sshkm.Group')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sshkm.Host')),
                ('osuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sshkm.Osuser')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('value', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='key',
            name='member_of',
            field=models.ManyToManyField(blank=True, through='sshkm.KeyGroup', to='sshkm.Group'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, through='sshkm.KeyGroup', to='sshkm.Key'),
        ),
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together=set([('group', 'host', 'osuser')]),
        ),
    ]
