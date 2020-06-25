# Generated by Django 3.0.4 on 2020-03-12 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('short_name', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('short_description', models.CharField(max_length=500)),
                ('img_thumb', models.CharField(max_length=500)),
                ('img_full', models.CharField(max_length=500)),
                ('rank', models.IntegerField()),
                ('mycategory', models.CharField(max_length=500)),
                ('realcategory', models.CharField(max_length=500)),
                ('subcategory', models.CharField(max_length=500)),
                ('date', models.DateField(auto_now=True)),
                ('pageviews', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('video', models.CharField(max_length=500)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('rating', models.IntegerField(default=0)),
                ('homepage', models.CharField(max_length=500)),
                ('reflink', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PriceLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('clicks', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link', to='products.Product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='products.Product')),
            ],
        ),
    ]