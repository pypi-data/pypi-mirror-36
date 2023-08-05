# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-31 12:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devilry_comment', '0009_auto_20180509_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentEditHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_edit_text', models.TextField(blank=True, default='')),
                ('pre_edit_text', models.TextField(blank=True, default='')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devilry_comment.Comment')),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
