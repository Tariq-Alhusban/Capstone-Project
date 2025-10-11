from django import forms
from .models import Food, FoodCategory

class CustomFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'category', 'calories', 'protein', 'carbs', 'fats', 'fiber', 'sodium']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Food name'}),
            'category': forms.Select(attrs={'class': 'form-input form-select'}),
            'calories': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'protein': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.1}),
            'carbs': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.1}),
            'fats': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.1}),
            'fiber': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.1}),
            'sodium': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.1}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select Category"
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input'})
