# Generated by Django 3.0.5 on 2020-10-17 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_order_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ip_address',
        ),
    ]
