from django import forms
from django.utils import timezone
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'plated_end_at']

    def clean_plated_end_at(self):
        plated_end_at = self.cleaned_data['plated_end_at']
        # Получение текущей даты и времени
        today = timezone.now()
        # Сравнение дат и времени
        if plated_end_at < today:
            raise forms.ValidationError("Plated end date cannot be in the past.")
        return plated_end_at