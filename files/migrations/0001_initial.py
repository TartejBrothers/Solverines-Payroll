# Generated by Django 5.0.4 on 2024-05-02 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Values',
            fields=[
                ('name', models.TextField()),
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('dept', models.TextField()),
                ('email', models.TextField()),
                ('phone', models.TextField()),
                ('salary', models.IntegerField()),
            ],
        ),
    ]
