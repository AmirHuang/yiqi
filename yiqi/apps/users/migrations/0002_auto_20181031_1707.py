# Generated by Django 2.0.2 on 2018-10-31 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='UserProFilebg/avatar/%y/%d/e744f4e5eb8b49b3ace5ee50bd7beabc'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='background',
            field=models.ImageField(blank=True, default='/default/default.jpg', null=True, upload_to='UserProFilebg/%Y/%m/e744f4e5eb8b49b3ace5ee50bd7beabc', verbose_name='背景图'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_bh',
            field=models.CharField(default='12dbcff9ab5a417c88a84306a47e3d59', max_length=50, unique=True, verbose_name='用户唯一ID'),
        ),
    ]
