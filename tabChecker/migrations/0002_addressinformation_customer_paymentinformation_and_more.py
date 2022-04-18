# Generated by Django 4.0.1 on 2022-04-18 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabChecker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('tabChecker.user',),
        ),
        migrations.CreateModel(
            name='PaymentInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccv', models.CharField(max_length=3)),
                ('expirationDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used', models.BooleanField(default=False)),
                ('eventID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tabChecker.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tabChecker.customer')),
            ],
        ),
    ]
