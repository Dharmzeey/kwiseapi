from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_rename_uk_used_to_foreign_used"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="series",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
    ]
