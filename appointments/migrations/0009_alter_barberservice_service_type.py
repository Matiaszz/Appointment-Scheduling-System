# Generated by Django 5.1.4 on 2024-12-11 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0008_remove_barberservice_payment_status_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barberservice',
            name='service_type',
            field=models.CharField(choices=[('hair', 'Cabelo'), ('eyebrow', 'Sobrancelha'), ('beard', 'Barba'), ('kids_haircut', 'Corte infantil'), ('hair_treatment', 'Tratamento capilar'), ('custom', 'Personalizado')], default='hair', max_length=30, verbose_name='Tipo de serviço'),
        ),
    ]
