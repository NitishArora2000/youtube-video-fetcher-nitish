# Generated by Django 4.2.11 on 2024-03-29 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('published_at', models.DateTimeField()),
                ('thumbnail_default', models.URLField()),
                ('thumbnail_medium', models.URLField()),
                ('thumbnail_high', models.URLField()),
            ],
            options={
                'indexes': [models.Index(fields=['published_at'], name='published_at_idx'), models.Index(fields=['title', 'description'], name='title_desc_idx')],
            },
        ),
    ]
