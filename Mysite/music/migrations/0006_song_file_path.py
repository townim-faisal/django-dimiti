# Generated by Django 2.1.7 on 2019-02-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_remove_song_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='file_path',
            field=models.CharField(default='#', max_length=500),
            preserve_default=False,
        ),
    ]
