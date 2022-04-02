# Generated by Django 4.0.1 on 2022-04-01 09:54

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('tabChecker', '0003_alter_attendees_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MemberSheetUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='upload/')),
                ('uploaded_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='Organizaer',
        ),
        migrations.AddField(
            model_name='event',
            name='AttendingOrgs',
            field=models.ManyToManyField(to='tabChecker.Organization'),
        ),
        migrations.AddField(
            model_name='organization',
            name='Organizer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tabChecker.organizer'),
        ),
        migrations.DeleteModel(
            name='Attendee',
        ),
        migrations.AddField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(to='tabChecker.Members'),
        ),
    ]