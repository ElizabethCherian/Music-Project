# Generated by Django 3.2.5 on 2021-10-11 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0004_song_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio',
            field=models.FileField(null=True, upload_to='Audios/'),
        ),
    ]