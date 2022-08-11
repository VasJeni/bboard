# Generated by Django 3.0 on 2022-08-10 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='is_activated',
            field=models.BooleanField(db_index=True, default=True, verbose_name='is activated?'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]