# Generated by Django 4.2.4 on 2023-09-11 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Accounts', '0003_alter_customuser_aadhar_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=17, null=True),
        ),
    ]
