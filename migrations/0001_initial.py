# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import uuidfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MailContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='registrador_de_contacto')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='Contacto')),
            ],
        ),
        migrations.CreateModel(
            name='MailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('subject', models.CharField(verbose_name='Asunto', max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('uuid', uuidfield.fields.UUIDField(blank=True, editable=False, unique=True, max_length=32)),
                ('readed', models.BooleanField(default=False)),
                ('sended', models.BooleanField(default=False)),
                ('sended_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message', ckeditor.fields.RichTextField(blank=True)),
                ('important', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='destinatario', null=True)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='enviante')),
            ],
        ),
    ]
