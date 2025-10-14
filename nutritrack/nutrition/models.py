from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

 #1 FoodCategory Model
class FoodCategory(models.Model):
    name = models.CharField(max_length=50, unique=True) #uniqueness for the values
    icon = models.CharField(max_length=20, blank=True) #empty value for django forms not null string
    
    class Meta:
        verbose_name_plural = "Food Categories" # override automatic pluralization
        ordering = ['name']
    
    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name

  #2 Food Model
class Food(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Nutrition per 100g
    # ensures a field's value is never less than zero.
    calories = models.IntegerField(validators=[MinValueValidator(0)])
    protein = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    carbs = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    fats = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    fiber = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    sodium = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    # Custom food tracking
    is_custom = models.BooleanField(default=False) #user manually added this food
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #Tracks who created it
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.calories} cal/100g)"

   #3 MealPlan Model
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    goal_calories = models.IntegerField(default=2000, validators=[MinValueValidator(1000)])
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 #Each user can have one meal plan per day.
 #Used to store their calorie goal and notes.    

    class Meta:   # no duplicate plans for the same date.   
        unique_together = ('user', 'date')
        ordering = ['-date']
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    def total_calories(self):
        return sum(entry.scaled_calories() for entry in self.mealentry_set.all()) #all calories from the foods eaten that day adds up.
    
    def calories_remaining(self):
        return self.goal_calories - self.total_calories()
    
    def total_protein(self):
        return round(sum(entry.scaled_protein() for entry in self.mealentry_set.all()), 1)
    
    def total_carbs(self):
        return round(sum(entry.scaled_carbs() for entry in self.mealentry_set.all()), 1)
    
    def total_fats(self):
        return round(sum(entry.scaled_fats() for entry in self.mealentry_set.all()), 1)
    
    def progress_percentage(self):
        return min(100, round((self.total_calories() / self.goal_calories) * 100))
 #4 MealEntry Model       
class MealEntry(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    UNIT_CHOICES = [
        ('g', 'Grams'),
        ('ml', 'Milliliters'),
        ('cup', 'Cup'),
        ('tbsp', 'Tablespoon'),
        ('tsp', 'Teaspoon'),
        ('piece', 'Piece'),
        ('serving', 'Serving'),
    ]
    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    quantity = models.FloatField(default=100, validators=[MinValueValidator(0.1)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='g')
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['meal_type', 'added_at']
    
    def __str__(self):
        return f"{self.meal_plan.date} - {self.meal_type}: {self.food.name}"
    
    def get_scale_factor(self):
        # Convert different units to 100g equivalent
        if self.unit == 'g':
            return self.quantity / 100
        elif self.unit == 'cup':
            return self.quantity * 2.4  # Approximate conversion
        elif self.unit == 'tbsp':
            return self.quantity * 0.15
        else:
            return self.quantity  # Default for pieces/servings
    
    def scaled_calories(self):
        return round(self.food.calories * self.get_scale_factor())
    
    def scaled_protein(self):
        return (self.food.protein or 0) * self.get_scale_factor()
    
    def scaled_carbs(self):
        return (self.food.carbs or 0) * self.get_scale_factor()
    
    def scaled_fats(self):
        return (self.food.fats or 0) * self.get_scale_factor()

 #5 RecipeTemplate Model
class RecipeTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    ingredients = models.ManyToManyField(Food, through='RecipeIngredient')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.user.username}'s {self.name}"
    
    def total_calories(self):
        return sum(ing.scaled_calories() for ing in self.recipeingredient_set.all())
    
    def ingredient_count(self):
        return self.recipeingredient_set.count()
  #6 RecipeIngredient Model
class RecipeIngredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'Grams'),
        ('ml', 'Milliliters'),
        ('cup', 'Cup'),
        ('tbsp', 'Tablespoon'),
        ('tsp', 'Teaspoon'),
        ('piece', 'Piece'),
        ('serving', 'Serving'),
    ]
    
    recipe = models.ForeignKey(RecipeTemplate, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0.1)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    notes = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ('recipe', 'food')
    
    def __str__(self):
        return f"{self.recipe.name}: {self.quantity}{self.unit} {self.food.name}"
    
    def get_scale_factor(self):
        if self.unit == 'g':
            return self.quantity / 100
        elif self.unit == 'cup':
            return self.quantity * 2.4
        elif self.unit == 'tbsp':
            return self.quantity * 0.15
        else:
            return self.quantity
    
    def scaled_calories(self):
        return round(self.food.calories * self.get_scale_factor())
