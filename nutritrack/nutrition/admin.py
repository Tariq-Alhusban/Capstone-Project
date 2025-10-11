from django.contrib import admin
from django.utils.html import format_html
from .models import FoodCategory, Food, MealPlan, MealEntry, RecipeTemplate, RecipeIngredient

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'food_count']
    search_fields = ['name']
    
    def food_count(self, obj):
        return obj.food_set.count()
    food_count.short_description = 'Foods'

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories', 'protein', 'is_custom', 'created_by']
    list_filter = ['category', 'is_custom', 'created_by']
    search_fields = ['name', 'category__name']
    ordering = ['category', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'is_custom', 'created_by')
        }),
        ('Nutrition (per 100g)', {
            'fields': ('calories', 'protein', 'carbs', 'fats', 'fiber', 'sodium')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class MealEntryInline(admin.TabularInline):
    model = MealEntry
    extra = 0
    fields = ['food', 'meal_type', 'quantity', 'unit']

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'goal_calories', 'total_calories', 'progress_bar']
    list_filter = ['date', 'user']
    ordering = ['-date']
    inlines = [MealEntryInline]
    
    def progress_bar(self, obj):
        percentage = obj.progress_percentage()
        color = 'green' if percentage >= 80 else 'orange' if percentage >= 60 else 'red'
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0;">'
            '<div style="width: {}px; background-color: {}; height: 20px;"></div></div>',
            percentage, color
        )
    progress_bar.short_description = 'Progress'

@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ['meal_plan', 'food', 'meal_type', 'quantity', 'unit', 'scaled_calories']
    list_filter = ['meal_type', 'meal_plan__date', 'food__category']
    search_fields = ['food__name', 'meal_plan__user__username']

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ['food', 'quantity', 'unit', 'notes']

@admin.register(RecipeTemplate)
class RecipeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'ingredient_count', 'total_calories', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'description']
    inlines = [RecipeIngredientInline]

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'food', 'quantity', 'unit', 'scaled_calories']
    list_filter = ['recipe', 'food__category']
