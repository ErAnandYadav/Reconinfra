# Generated by Django 4.2.4 on 2023-10-02 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0022_rename_cheque_number_emihistory_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='emihistory',
            name='booking_status',
            field=models.CharField(choices=[('Saved', 'Saved'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved')], default='Saved', max_length=100, null=True),
        ),
    ]