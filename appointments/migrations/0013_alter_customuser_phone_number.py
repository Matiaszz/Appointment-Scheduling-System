# Generated by Django 5.1.4 on 2024-12-12 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0012_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='', max_length=11, verbose_name='Número de telefone'),
        ),
    ]
