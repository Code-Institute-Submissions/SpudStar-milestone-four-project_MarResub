# Generated by Django 3.2 on 2022-01-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20220116_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_email',
            field=models.CharField(blank=True, default='xx@gmail.com', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='default_trainer_code',
            field=models.CharField(blank=True, default='XXX-XXXX-XXX', max_length=20),
        ),
    ]
