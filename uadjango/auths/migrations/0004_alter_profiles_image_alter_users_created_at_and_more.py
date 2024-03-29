# Generated by Django 5.0.3 on 2024-03-22 07:12

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_alter_users_created_at_alter_users_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='image',
            field=models.URLField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 7, 12, 58, 348601, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('f09c0456-f1ec-4916-88ba-bd1eefba3c10'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 7, 12, 58, 348601, tzinfo=datetime.timezone.utc)),
        ),
    ]
