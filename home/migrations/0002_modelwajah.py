# Generated by Django 4.0.6 on 2022-07-06 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelWajah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.FileField(upload_to='media/model/')),
                ('total_data', models.CharField(max_length=4)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
