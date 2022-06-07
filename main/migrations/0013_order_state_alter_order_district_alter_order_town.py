# Generated by Django 4.0.4 on 2022-06-07 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_order_area_order_district_order_province_order_town'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(default='processing', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='district',
            field=models.CharField(default='bhaktapur', max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='town',
            field=models.CharField(default='thimi', max_length=200),
        ),
    ]