# Generated by Django 4.1.4 on 2023-09-11 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0004_rename_agent_wallet_associate_remove_wallet_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotbooking',
            name='emi_period',
            field=models.CharField(blank=True, choices=[('12', '12 Months'), ('24', '24 Months'), ('36', '36 Months'), ('48', '48 Months'), ('60', '60 Months')], default=0, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='plotbooking',
            name='plot_number',
            field=models.CharField(error_messages={'unique': 'This plot number has been already booked!'}, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='plotbooking',
            name='remaining_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]