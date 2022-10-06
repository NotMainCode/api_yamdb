# Generated by Django 2.2.16 on 2022-10-05 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_user_confirmation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="confirmation_code",
            field=models.CharField(
                blank=True, max_length=75, verbose_name="First name"
            ),
        ),
    ]
