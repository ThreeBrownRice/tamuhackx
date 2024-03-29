# Generated by Django 5.0.1 on 2024-01-28 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc_time', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='storeType',
            new_name='shop_type',
        ),
        migrations.AlterField(
            model_name='shop',
            name='tags',
            field=models.ManyToManyField(related_name='shops', to='misc_time.tag'),
        ),
    ]
