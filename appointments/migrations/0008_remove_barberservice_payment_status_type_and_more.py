# Generated by Django 5.1.4 on 2024-12-10 22:49

import appointments.utils.validations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_barberservice_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barberservice',
            name='payment_status_type',
        ),
        migrations.AddField(
            model_name='barberservice',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descrição do serviço'),
        ),
        migrations.AddField(
            model_name='barberservice',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Duração (minutos)'),
        ),
        migrations.AddField(
            model_name='barberservice',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Imagem do serviço'),
        ),
        migrations.AddField(
            model_name='barberservice',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Serviço Ativo'),
        ),
        migrations.AlterField(
            model_name='barberservice',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[appointments.utils.validations.validate_positive_price], verbose_name='Preço'),
        ),
        migrations.AlterField(
            model_name='barberservice',
            name='service_type',
            field=models.CharField(choices=[('hair', 'Cabelo'), ('beard', 'Barba'), ('kids_haircut', 'Corte infantil'), ('hair_treatment', 'Tratamento capilar'), ('custom', 'Personalizado')], default='hair', max_length=30, verbose_name='Tipo de serviço'),
        ),
    ]