# Generated by Django 2.0.2 on 2018-11-06 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SharingSet', '0006_auto_20181103_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharingsetmodel',
            name='imageUrl',
            field=models.ImageField(blank=True, null=True, upload_to='SharingSet/%y/%d/47e421f5f6e54b60bc2cde21335c604a', verbose_name='分享图片'),
        ),
        migrations.AlterField(
            model_name='sharingsetmodel',
            name='set_path',
            field=models.CharField(choices=[('3', '发现页面'), ('0', '通用页面'), ('2', '发布页面'), ('5', '内容页面'), ('1', '活动页面'), ('4', '消息页面')], default='0', max_length=1, verbose_name='分享页面设置'),
        ),
    ]