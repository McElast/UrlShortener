from django import forms

from .models import ShortenUrl
from configs import DOMAIN_URL


class ShortenUrlForm(forms.ModelForm):
    """
    Форма для создания сокращенных ссылок на основании модели ShortenUrl
    """
    class Meta:
        model = ShortenUrl
        fields = ['original_url', 'short_url_part']
        labels = {
            'original_url': 'Ваша ссылка (***обязательное поле)',
            'short_url_part': f'Новая ссылка >> {DOMAIN_URL}xxxxxxxxxx'
        }
        widgets = {
            'original_url': forms.URLInput(attrs={'placeholder': 'До 1000 символов'}),
            'short_url_part': forms.TextInput(attrs={'placeholder': 'Сократить (авто или вручную)'}),
        }
