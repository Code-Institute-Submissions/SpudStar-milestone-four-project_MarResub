# Generated by Django 3.2 on 2022-01-15 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('goods', '0004_auto_20211209_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='owner_profile',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='owner_profile',
                                    to='profiles.userprofile'),
        ),
    ]
