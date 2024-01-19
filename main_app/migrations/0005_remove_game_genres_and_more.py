# Generated by Django 5.0.1 on 2024-01-18 01:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0004_userprofile_liked_games"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="genres",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="preferred_genres",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="liked_games",
        ),
        migrations.AddField(
            model_name="game",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="game",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="genres",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="Genre",
        ),
    ]
