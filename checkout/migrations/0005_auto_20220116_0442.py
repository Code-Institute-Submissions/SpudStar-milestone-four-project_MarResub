# Generated by Django 3.2 on 2022-01-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20220115_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_trainer_code',
            field=models.CharField(max_length=20),
        ),
    ]