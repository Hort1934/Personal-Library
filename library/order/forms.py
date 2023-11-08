from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'user', 'plated_end_at']

    def clean_plated_end_at(self):
        plated_end_at = self.cleaned_data['plated_end_at']
        # Додайте додаткову валідацію, якщо потрібно
        return plated_end_at
