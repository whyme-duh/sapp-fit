# Generated by Django 4.1.4 on 2023-01-05 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_remove_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutandquote',
            name='backgroundImage',
            field=models.ImageField(null=True, upload_to='images/bg'),
        ),
        migrations.AddField(
            model_name='aboutandquote',
            name='profileImage',
            field=models.ImageField(null=True, upload_to='images/bg'),
        ),
    ]
