# Generated by Django 2.1.5 on 2019-02-05 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_date', models.DateTimeField()),
                ('home_team', models.CharField(max_length=120)),
                ('away_team', models.CharField(max_length=120)),
                ('soccerway_url', models.CharField(max_length=255)),
                ('betin_url', models.CharField(max_length=255)),
                ('table_score', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('p_table_score', models.CharField(max_length=50)),
                ('last_five_score', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('p_last_five_score', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Home',
            },
        ),
    ]
