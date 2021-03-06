# Generated by Django 3.0.5 on 2020-10-16 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201016_1410'),
        ('checkout', '0002_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_address_1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_address_2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_zip',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address_1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address_2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_zip',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.UserDefaultAddress'),
        ),
    ]
