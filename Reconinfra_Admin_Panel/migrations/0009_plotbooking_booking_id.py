# Generated by Django 4.2.4 on 2023-09-16 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0008_alter_plotbooking_emi_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotbooking',
            name='booking_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
