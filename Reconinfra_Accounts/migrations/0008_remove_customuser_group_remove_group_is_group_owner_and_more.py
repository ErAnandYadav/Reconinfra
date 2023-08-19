# Generated by Django 4.1 on 2023-01-22 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Accounts', '0007_remove_group_agent_customuser_group_group_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='group',
        ),
        migrations.RemoveField(
            model_name='group',
            name='is_group_owner',
        ),
        migrations.CreateModel(
            name='GroupInitialize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Reconinfra_Accounts.group')),
            ],
        ),
    ]