# Generated by Django 4.1.13 on 2024-03-01 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_remove_message_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
