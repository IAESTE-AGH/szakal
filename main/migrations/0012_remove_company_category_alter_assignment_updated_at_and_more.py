# Generated by Django 4.1.2 on 2022-10-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_company_category_company_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='category',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='contactperson',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
