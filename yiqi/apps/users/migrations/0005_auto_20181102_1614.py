# Generated by Django 2.0.2 on 2018-11-02 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181102_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='UserProFilebg/avatar/%y/%d/d310063d3df24b6cabf0f1afa864697c'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='background',
            field=models.ImageField(blank=True, default='/default/default.jpg', null=True, upload_to='UserProFilebg/%Y/%m/d310063d3df24b6cabf0f1afa864697c', verbose_name='背景图'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_bh',
            field=models.CharField(default='84bb055aeb5a4f4e9fd6a1a04f4db9ed', max_length=50, unique=True, verbose_name='用户唯一ID'),
        ),
    ]
