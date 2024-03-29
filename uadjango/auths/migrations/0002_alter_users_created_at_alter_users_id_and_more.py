# Generated by Django 5.0.3 on 2024-03-22 05:20

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 5, 20, 13, 944302, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('bceab804-549d-4a93-8e88-267301f842b2'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 5, 20, 13, 944302, tzinfo=datetime.timezone.utc)),
        ),
    ]
