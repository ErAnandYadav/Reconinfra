# Generated by Django 4.2.4 on 2023-09-11 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Accounts', '0002_alter_customuser_pan_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='aadhar_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]