# Generated by Django 3.2 on 2023-01-31 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230131_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='category',
        ),
        migrations.AddField(
            model_name='title',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='titles', to='reviews.category'),
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='reviews.TitleGenre', to='reviews.Genre'),
        ),
    ]
