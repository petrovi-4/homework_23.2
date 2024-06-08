from django import forms

from catalog.models import Product, Version
from config.settings import FORBIDDEN_WORDS


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if set(product_name.lower().split()).intersection(set(FORBIDDEN_WORDS)):
            raise forms.ValidationError('Нельзя использовать запрещенные слова')
        return product_name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if set(description.lower().split()).intersection(set(FORBIDDEN_WORDS)):
            raise forms.ValidationError('Нельзя использовать запрщенные слова')
        if len(description) < 10 or len(description) > 200:
            raise forms.ValidationError('Описание должно быть от 10 до 200 символов')
        return description


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published', )


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
