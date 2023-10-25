# Generated by Django 4.2.4 on 2023-10-24 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0026_alter_plotnumber_properties_plotavailabilities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotavailabilities',
            name='plot_status',
            field=models.CharField(choices=[('hold', 'Hold'), ('available', 'Available'), ('booked', 'Booked'), ('registerd', 'Registerd'), ('pending', 'Pending')], default='Available', max_length=100, null=True),
        ),
    ]