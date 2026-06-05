from django.db import migrations


def rename_uk_used(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    Product.objects.filter(status="UK-Used").update(status="Foreign Used")


def reverse_rename(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    Product.objects.filter(status="Foreign Used").update(status="UK-Used")


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_add_product_image"),
    ]

    operations = [
        migrations.RunPython(rename_uk_used, reverse_rename),
    ]
