from django.forms import ModelForm, ValidationError

from catalog.mixins import StyleFormMixin
from catalog.models import Product, Version

BAD_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "image",
            "category",
            "price",
        )

    def __validate_data(self, data) -> None:
        for bad_word in BAD_WORDS:
            if bad_word in data:
                raise ValidationError(f"Нельзя использовать '{bad_word}'")

    def clean_title(self):
        data = self.cleaned_data["title"]
        self.__validate_data(data)
        return data

    def clean_description(self):
        data = self.cleaned_data["description"]
        self.__validate_data(data)
        return data


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = (
            "major",
            "build",
            "product",
            "is_active",
        )
