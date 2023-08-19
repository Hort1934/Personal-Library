from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'user', 'plated_end_at', 'end_at']  # Include the 'end_at' field for editing

    def clean_end_at(self):
        end_at = self.cleaned_data['end_at']
        # Add any additional validation or custom logic for the 'end_at' field
        return end_at