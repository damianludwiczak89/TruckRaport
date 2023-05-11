# Generated by Django 4.1.1 on 2023-04-24 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("truck", "0005_spedition_alter_tour_spedition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tour",
            name="spedition",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="sped",
                to="truck.spedition",
            ),
        ),
        migrations.AlterField(
            model_name="tour",
            name="truck",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="truck.truck"
            ),
        ),
    ]