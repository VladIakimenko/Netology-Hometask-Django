# Generated by Django 4.2.1 on 2023-05-29 15:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertisements', '0002_alter_advertisement_id_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'advertisement')},
        ),
    ]
