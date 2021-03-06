# Generated by Django 2.0.2 on 2018-10-31 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20181031_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityimagesmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ActivityImagesModel/%y/%d/ea64a57bcf2f4fd381adcf007f9d1548', verbose_name='活动图片'),
        ),
        migrations.AlterField(
            model_name='activitymodel',
            name='audit',
            field=models.CharField(choices=[('1', '审核通过'), ('0', '审核中')], default=0, max_length=1, verbose_name='审核状态'),
        ),
        migrations.AlterField(
            model_name='activitymodel',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='Activity/%y/%d/ea64a57bcf2f4fd381adcf007f9d1548', verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='activitymodel',
            name='groupcode',
            field=models.ImageField(blank=True, null=True, upload_to='Activity/qr/%y/%d/ea64a57bcf2f4fd381adcf007f9d1548', verbose_name='群二维码'),
        ),
        migrations.AlterField(
            model_name='activitytypemodel',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='ActivityTypeModel/%y/%d/ea64a57bcf2f4fd381adcf007f9d1548', verbose_name='类别图片'),
        ),
        migrations.AlterField(
            model_name='slidemodels',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='SlideModels/%y/%d/ea64a57bcf2f4fd381adcf007f9d1548', verbose_name='幻灯片图片'),
        ),
    ]
