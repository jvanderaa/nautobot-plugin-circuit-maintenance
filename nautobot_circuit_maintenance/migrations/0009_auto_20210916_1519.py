# Generated by Django 3.1.13 on 2021-09-16 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("circuits", "0002_initial_part_2"),
        ("nautobot_circuit_maintenance", "0008_raw_binary"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="rawnotification",
            unique_together={("date", "provider", "subject")},
        ),
        migrations.RemoveField(
            model_name="rawnotification",
            name="_raw_md5",
        ),
    ]
