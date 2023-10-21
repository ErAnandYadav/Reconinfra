# Generated by Django 4.2.4 on 2023-09-11 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Accounts', '0004_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='aadhar_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='pan_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=17, null=True, unique=True),
        ),
    ]
