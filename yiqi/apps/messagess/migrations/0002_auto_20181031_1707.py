# Generated by Django 2.0.2 on 2018-10-31 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagess', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysusermodel',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='SysUserModel/%Y/%m/974bc8a61d9f4a2ea8b933b1a3544502', verbose_name='系统用户头像'),
        ),
    ]
