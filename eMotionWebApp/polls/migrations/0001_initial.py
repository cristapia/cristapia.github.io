# Generated by Django 4.0.5 on 2023-10-13 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('restriccion', models.BooleanField(default=False)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Capitulos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo_capitulo', models.CharField(max_length=100)),
                ('contenido', models.TextField()),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capitulos', to='polls.obra')),
            ],
        ),
    ]
