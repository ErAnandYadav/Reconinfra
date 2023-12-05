# Generated by Django 4.2.4 on 2023-11-25 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reconinfra_Admin_Panel', '0031_wallet_plot_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimedReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Requested', 'Requested'), ('Completed', 'Completed')], max_length=100, null=True)),
                ('associate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reward', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Reconinfra_Admin_Panel.reward')),
            ],
        ),
    ]