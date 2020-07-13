# Generated by Django 2.2.13 on 2020-07-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('subjects', '0001_initial'), ('subjects', '0002_auto_20200405_1101'), ('subjects', '0003_auto_20200520_1844'), ('subjects', '0004_auto_20200520_1901'), ('subjects', '0005_auto_20200521_1702')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Title')),
                ('type', models.CharField(choices=[('book', 'Book'), ('movie', 'Movie'), ('doc', 'Documentary'), ('website', 'Website'), ('yt_channel', 'Youtube Channel'), ('social_media', 'Social Media'), ('other', 'Other')], default='other', max_length=20, verbose_name='Content Type')),
                ('creator', models.CharField(blank=True, max_length=255, verbose_name='Creator')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('link', models.URLField(blank=True, verbose_name='Link')),
                ('subject', models.ManyToManyField(to='subjects.Subject')),
                ('image', models.ImageField(blank=True, null=True, upload_to='content_images', verbose_name='Image')),
            ],
        ),
    ]
