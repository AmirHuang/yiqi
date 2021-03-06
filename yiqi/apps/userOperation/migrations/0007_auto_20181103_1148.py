# Generated by Django 2.0.2 on 2018-11-03 11:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_auto_20181103_1148'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userOperation', '0006_auto_20181102_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackmodels',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='FeedBackModels/%y/%d/4d073979383e4baba75db24ee33affb7', verbose_name='反馈图片'),
        ),
        migrations.AlterUniqueTogether(
            name='collectionusermodel',
            unique_together={('user', 'activity')},
        ),
    ]
