# Generated by Django 2.2.13 on 2020-07-13 07:02

from django.db import migrations
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0026_auto_20200712_1749'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tagulous_Content_tags',
        ),
        migrations.AlterField(
            model_name='content',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, force_lowercase=True, help_text='Enter a comma-separated tag string', initial='technology, entrepreneurship, self-development, self-growth', related_name='content_tag', to='common.Tags'),
        ),
    ]