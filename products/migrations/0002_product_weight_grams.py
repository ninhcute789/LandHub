# Generated by Django 5.1.4 on 2025-04-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="weight_grams",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
