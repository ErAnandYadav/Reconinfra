# Generated by Django 4.1 on 2022-11-25 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sortname', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Reconinfra_Accounts.country')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=17, null=True, unique=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='Recon/User/Profile-Picture')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_facilitator', models.BooleanField(default=False)),
                ('is_accountent', models.BooleanField(default=False)),
                ('aadhar_number', models.CharField(max_length=20, null=True, unique=True)),
                ('aadhar_front', models.ImageField(blank=True, null=True, upload_to='Recon/User/Aadhar')),
                ('aadhar_back', models.ImageField(blank=True, null=True, upload_to='Recon/User/Aadhar')),
                ('pan_number', models.CharField(max_length=11, null=True, unique=True)),
                ('pan_front', models.ImageField(blank=True, null=True, upload_to='Recon/User/PAN')),
                ('pan_back', models.ImageField(blank=True, null=True, upload_to='Recon/User/PAN')),
                ('account_holder_name', models.CharField(max_length=50, null=True)),
                ('account_number', models.CharField(max_length=25, null=True)),
                ('account_type', models.CharField(choices=[('Saving', 'Saving'), ('Current', 'Current')], default='Saving', max_length=50, null=True)),
                ('ifsc_code', models.CharField(max_length=15, null=True)),
                ('bank_name', models.CharField(max_length=50, null=True)),
                ('branch_name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=150, null=True)),
                ('sponsor_id', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Reconinfra_Accounts.city')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Reconinfra_Accounts.country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('referred_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Reconinfra_Accounts.state')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Reconinfra_Accounts.state'),
        ),
    ]
