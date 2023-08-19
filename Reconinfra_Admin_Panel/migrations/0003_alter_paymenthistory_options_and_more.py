# Generated by Django 4.1 on 2022-11-28 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reconinfra_Admin_Panel', '0002_plotbooking_booking_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymenthistory',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='plotbooking',
            name='down_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='plotbooking',
            name='emi_period',
            field=models.CharField(choices=[('12', '12 Months'), ('18', '18 Months')], default='12 Months', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='plotbooking',
            name='payment_method',
            field=models.CharField(choices=[('Full Payment', 'Full Payment'), ('EMI', 'EMI')], default='EMI', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='plotbooking',
            name='pin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='plotbooking',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]