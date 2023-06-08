# Generated by Django 4.1.7 on 2023-06-08 16:26

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('idols', '0002_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2, '이름은 2자 이상이어야합니다.')])),
                ('nickname', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(3, '닉네임은 3자 이상이어야합니다.')])),
                ('email', models.EmailField(error_messages={'unique': '이미 사용중인 이메일입니다.'}, max_length=100, unique=True, verbose_name='Email-address')),
                ('profileImg', models.URLField(blank=True, default='https://api.cloudflare.com/client/v4/accounts/135e63e511ff302b43eaab2356b50bf6/images/v1/fccba4a0-df32-485d-8c6f-9410b97c2100', null=True)),
                ('age', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(15, '15세 이상부터 가입이 가능합니다.')])),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('pick', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='idols.idol')),
            ],
            options={
                'verbose_name_plural': 'Our_Users',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('category_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='categories.category')),
                ('title', models.CharField(default='', max_length=100)),
                ('location', models.CharField(default='', max_length=100)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('owner', models.ForeignKey(default='', max_length=100, on_delete=django.db.models.deletion.CASCADE, related_name='report', to=settings.AUTH_USER_MODEL)),
                ('whoes', models.ManyToManyField(blank=True, null=True, related_name='report', to='idols.idol')),
            ],
            options={
                'verbose_name_plural': 'User Report',
            },
            bases=('categories.category',),
        ),
        migrations.AddField(
            model_name='user',
            name='reports',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to='users.report'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
