# Generated by Django 4.2.4 on 2023-10-02 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0023_emihistory_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emihistory',
            name='payment_method',
            field=models.CharField(choices=[('Cheque', 'Cheque'), ('DD', 'DD'), ('Cash', 'Cash'), ('NEFT/IMPS/RTGS', 'NEFT/IMPS/RTGS')], default='N/A', max_length=100, null=True),
        ),
    ]
