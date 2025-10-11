from django import forms
from .models import Food, FoodCategory
from .models import MealEntry


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

class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ['food', 'meal_type', 'quantity', 'unit']
        widgets = {
            'food': forms.Select(attrs={'class': 'form-input form-select'}),
            'meal_type': forms.Select(attrs={'class': 'form-input form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': 0.1, 'step': 0.1}),
            'unit': forms.Select(attrs={'class': 'form-input form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food'].queryset = Food.objects.select_related('category').order_by('category__name', 'name')
        
        # Make labels more user-friendly
        self.fields['food'].label = "Food Item"
        self.fields['meal_type'].label = "Meal"
        self.fields['quantity'].label = "Quantity"
        self.fields['unit'].label = "Unit"


from django.forms import inlineformset_factory

class RecipeTemplateForm(forms.ModelForm):
    class Meta:
        model = RecipeTemplate
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Recipe name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Recipe description or instructions'}),
        }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['food', 'quantity', 'unit', 'notes']
        widgets = {
            'food': forms.Select(attrs={'class': 'form-input form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': 0.1, 'step': 0.1}),
            'unit': forms.Select(attrs={'class': 'form-input form-select'}),
            'notes': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. diced, cooked'})
        }

# Create formset for multiple ingredients
RecipeIngredientFormSet = inlineformset_factory(
    RecipeTemplate, 
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=3,
    can_delete=True
)
