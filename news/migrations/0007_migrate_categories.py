from django.db import migrations, models
import django.db.models.deletion


def migrate_categories(apps, schema_editor):
    News = apps.get_model("news", "News")

    for news in News.objects.all():
        if news.category_new_id:
            news.category = str(news.category_new_id)
            news.save(update_fields=["category"])


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0006_news_category_new"),
    ]

    operations = [
        migrations.RunPython(migrate_categories),
        migrations.AlterField(
            model_name="news",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="news",
                to="news.category",
                verbose_name="Категория",
            ),
        ),
        migrations.RemoveField(
            model_name="news",
            name="category_new",
        ),
    ]
