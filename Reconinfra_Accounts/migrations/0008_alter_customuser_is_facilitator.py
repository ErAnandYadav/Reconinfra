# Generated by Django 4.2.4 on 2023-10-24 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Accounts', '0007_alter_customuser_referred_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_facilitator',
            field=models.BooleanField(default=True),
        ),
    ]