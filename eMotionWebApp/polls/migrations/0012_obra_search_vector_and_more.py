# Generated by Django 4.1 on 2023-11-13 00:36

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_usuario_facebook_usuario_instagram_usuario_tumblr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='obra',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='polls_obra_search__538942_gin'),
        ),
    ]
