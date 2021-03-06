# Generated by Django 2.0.2 on 2018-11-02 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userOperation', '0004_auto_20181102_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityuserinfo',
            name='type',
            field=models.CharField(choices=[('0', '活动发起人'), ('1', '活动参加人')], default='1', max_length=1, verbose_name='报名用户类型'),
        ),
        migrations.AlterField(
            model_name='feedbackmodels',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='FeedBackModels/%y/%d/ae5014ffa7ee4792b622448a5bdb8a41', verbose_name='反馈图片'),
        ),
    ]
