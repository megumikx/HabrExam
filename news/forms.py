from .models import News
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, FileInput


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "anons", "full_text", "category", "data", "image"]

        widgets = {
            "title": TextInput(
                attrs={"class": "form-control", "placeholder": "Название статьи"}
            ),
            "anons": TextInput(
                attrs={"class": "form-control", "placeholder": "Анонс статьи"}
            ),
            "data": DateTimeInput(
                attrs={"class": "form-control", "placeholder": "Дата публикации"}
            ),
            "full_text": Textarea(
                attrs={"class": "form-control", "placeholder": "Текст статьи"}
            ),
            "image": FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].empty_label = "Выберите категорию"
