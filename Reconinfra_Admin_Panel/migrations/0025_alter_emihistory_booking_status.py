# Generated by Django 4.2.4 on 2023-10-02 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0024_alter_emihistory_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emihistory',
            name='booking_status',
            field=models.CharField(blank=True, choices=[('Saved', 'Saved'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved')], default='Saved', max_length=100, null=True),
        ),
    ]