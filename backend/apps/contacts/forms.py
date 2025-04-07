from django import forms
from .models import Public_Contact

class Public_ContactForm(forms.ModelForm):
    class Meta:
        model = Public_Contact
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        for field in self.fields:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = ''
        return cleaned_data