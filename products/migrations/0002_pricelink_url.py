# Generated by Django 3.0.4 on 2020-03-12 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricelink',
            name='url',
            field=models.CharField(default='#', max_length=500),
            preserve_default=False,
        ),
    ]