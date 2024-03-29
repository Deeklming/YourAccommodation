# Generated by Django 5.0.3 on 2024-03-22 05:20

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auths', '0003_alter_users_created_at_alter_users_id_and_more'),
        ('posts', '0002_alter_comments_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 3, 22, 5, 20, 30, 806439, tzinfo=datetime.timezone.utc))),
                ('head_count', models.IntegerField(default=0)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('payment_price', models.DecimalField(decimal_places=6, max_digits=18)),
                ('post_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.posts')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auths.users')),
            ],
        ),
    ]
