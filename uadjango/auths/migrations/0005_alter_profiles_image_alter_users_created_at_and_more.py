# Generated by Django 5.0.3 on 2024-03-24 06:48

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0004_alter_profiles_image_alter_users_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='image',
            field=models.URLField(default=None, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 24, 6, 48, 13, 357495, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('1b6f5a40-1f4b-4021-b969-75787be47b3e'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 24, 6, 48, 13, 357495, tzinfo=datetime.timezone.utc)),
        ),
    ]
