# Generated by Django 2.2.7 on 2019-11-17 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupaccess', '0003_auto_20191115_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='fortiparameters',
            name='fortiCipheredData',
            field=models.CharField(default=None, max_length=128),
        ),
        migrations.AddField(
            model_name='fortiparameters',
            name='fortiCipheredIV',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
