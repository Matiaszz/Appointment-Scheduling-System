# Generated by Django 5.1.4 on 2024-12-10 19:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarberService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=50, verbose_name='Nome do serviço')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('service_type', models.CharField(choices=[('hair', 'Cabelo'), ('beard', 'Barba'), ('kids_haircut', 'Corte infantil'), ('hair_treatment', 'Tratamento capilar'), ('custom', 'Personalizado')], default='custom', max_length=30)),
                ('payment_status_type', models.CharField(choices=[('paid', 'Pago'), ('pending', 'Pendente'), ('canceled', 'Cancelado')], default='pending', max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', null=True, upload_to='profile_pictures/%Y/%m', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Foto de perfil'),
        ),
    ]