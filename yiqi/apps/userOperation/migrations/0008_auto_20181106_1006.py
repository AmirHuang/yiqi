# Generated by Django 2.0.2 on 2018-11-06 10:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity', '0008_auto_20181106_1006'),
        ('userOperation', '0007_auto_20181103_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackmodels',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='FeedBackModels/%y/%d/ebb1e8905ccc44fd8197d250319bcf8a', verbose_name='反馈图片'),
        ),
        migrations.AlterField(
            model_name='sysmessages',
            name='ISOPEN',
            field=models.CharField(choices=[('0', '未读'), ('1', '已读')], default='0', max_length=1, verbose_name='是否已读'),
        ),
        migrations.AlterUniqueTogether(
            name='reporttionusermodel',
            unique_together={('user', 'activity')},
        ),
    ]
