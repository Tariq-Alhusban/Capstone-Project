from django import template

register = template.Library()

@register.filter
def filter_by_meal_type(meal_entries, meal_type):
    """Filter meal entries by meal type (breakfast, lunch, dinner, snack)"""
    return meal_entries.filter(meal_type=meal_type)

@register.filter
def sum_calories(meal_entries):
    """Calculate total calories from meal entries"""
    total = 0
    for entry in meal_entries:
        total += (entry.food.calories * entry.quantity) / 100
    return round(total, 1)