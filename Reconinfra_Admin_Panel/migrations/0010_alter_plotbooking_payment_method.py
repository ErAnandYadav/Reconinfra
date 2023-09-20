# Generated by Django 4.2.4 on 2023-09-16 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0009_plotbooking_booking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotbooking',
            name='payment_method',
            field=models.CharField(choices=[('Cheque', 'Cheque'), ('DD', 'DD'), ('Cash', 'Cash'), ('Neft/imps/rtgs', 'Neft/imps/rtgs')], default='Cash', max_length=100, null=True),
        ),
    ]