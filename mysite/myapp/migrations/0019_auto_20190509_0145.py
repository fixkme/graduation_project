# Generated by Django 2.0.4 on 2019-05-08 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20190509_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Album')),
            ],
        ),
        migrations.RenameField(
            model_name='albumcomment',
            old_name='parent',
            new_name='origin_comment',
        ),
    ]