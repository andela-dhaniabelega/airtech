# Generated by Django 2.1.3 on 2018-12-04 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20181204_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='flight_number',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]