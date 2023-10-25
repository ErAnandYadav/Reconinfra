# Generated by Django 4.2.4 on 2023-10-24 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0027_alter_plotavailabilities_plot_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotavailabilities',
            name='plot_status',
            field=models.CharField(choices=[('hold', 'Hold'), ('available', 'Available'), ('booked', 'Booked'), ('registered', 'Registered'), ('pending', 'Pending')], default='available', max_length=100, null=True),
        ),
    ]
