# Generated by Django 2.0.2 on 2018-11-02 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagess', '0003_auto_20181102_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysusermodel',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='SysUserModel/%Y/%m/b7e857134ba5445f9b1dc91f6bd378ed', verbose_name='系统用户头像'),
        ),
    ]
