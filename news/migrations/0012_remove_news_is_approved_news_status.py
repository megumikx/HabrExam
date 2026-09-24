from django.db import migrations, models


def set_status_from_is_approved(apps, schema_editor):
    News = apps.get_model("news", "News")

    News.objects.filter(is_approved=True).update(status="approved")
    News.objects.filter(is_approved=False).update(status="pending")


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0011_news_is_approved"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "На проверке"),
                    ("approved", "Одобрено"),
                    ("rejected", "Отклонено"),
                ],
                default="pending",
                max_length=20,
                verbose_name="Статус",
            ),
        ),

        migrations.RunPython(
            set_status_from_is_approved,
            migrations.RunPython.noop,
        ),

        migrations.RemoveField(
            model_name="news",
            name="is_approved",
        ),
    ]