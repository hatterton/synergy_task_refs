# Generated by Django 4.2 on 2023-04-07 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('ref_level', models.IntegerField()),
                ('team_size', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='refs', to='refs.usermodel')),
            ],
        ),
    ]