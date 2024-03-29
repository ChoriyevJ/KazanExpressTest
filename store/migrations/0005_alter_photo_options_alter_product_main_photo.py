# Generated by Django 4.2.7 on 2024-02-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_alter_photo_options_photo_is_main"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="photo",
            options={"ordering": ["-is_main"]},
        ),
        migrations.AlterField(
            model_name="product",
            name="main_photo",
            field=models.ImageField(blank=True, editable=False, null=True, upload_to="images/"),
        ),
    ]
