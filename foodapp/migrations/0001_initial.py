# Generated by Django 5.1.2 on 2024-12-08 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('food_type', models.CharField(max_length=255)),
                ('quantity_kg', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('is_veg_preferred', models.BooleanField(default=True)),
                ('preferred_quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('number', models.CharField(max_length=50)),
                ('foodName', models.CharField(max_length=191)),
                ('food_type', models.CharField(choices=[('veg', 'Vegetarian'), ('nonveg', 'Non-Vegetarian')], max_length=6)),
                ('foodImage', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('food_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500, null=True)),
                ('expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to=settings.AUTH_USER_MODEL)),
                ('recipients', models.ManyToManyField(blank=True, related_name='allocated_donations', to='foodapp.recipient')),
            ],
        ),
    ]
