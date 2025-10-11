from django.core.management.base import BaseCommand
from nutrition.models import FoodCategory, Food

class Command(BaseCommand):
    help = 'Load comprehensive sample food data'
    
    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {"name": "Proteins", "icon": "🥩"},
            {"name": "Vegetables", "icon": "🥬"},
            {"name": "Fruits", "icon": "🍎"},
            {"name": "Grains & Starches", "icon": "🌾"},
            {"name": "Dairy", "icon": "🥛"},
            {"name": "Healthy Fats", "icon": "🥑"},
            {"name": "Beverages", "icon": "💧"},
            {"name": "Snacks", "icon": "🥜"}
        ]
        
        for cat_data in categories_data:
            category, created = FoodCategory.objects.get_or_create(
                name=cat_data["name"],
                defaults={"icon": cat_data["icon"]}
            )
            if created:
                self.stdout.write(f"✅ Created category: {category.name}")
        
        # Load foods with detailed nutrition
        self._load_foods()
        
        self.stdout.write(self.style.SUCCESS('🎉 Sample data loaded successfully!'))
    
    def _load_foods(self):
        # Get categories
        proteins = FoodCategory.objects.get(name="Proteins")
        vegetables = FoodCategory.objects.get(name="Vegetables")
        fruits = FoodCategory.objects.get(name="Fruits")
        grains = FoodCategory.objects.get(name="Grains & Starches")
        dairy = FoodCategory.objects.get(name="Dairy")
        fats = FoodCategory.objects.get(name="Healthy Fats")
        beverages = FoodCategory.objects.get(name="Beverages")
        snacks = FoodCategory.objects.get(name="Snacks")
        
        foods_data = [
            # Proteins (per 100g)
            {"name": "Chicken Breast (skinless)", "category": proteins, "calories": 165, "protein": 31.0, "carbs": 0.0, "fats": 3.6, "fiber": 0.0},
            {"name": "Salmon Fillet", "category": proteins, "calories": 208, "protein": 25.4, "carbs": 0.0, "fats": 12.4, "fiber": 0.0},
            {"name": "Greek Yogurt (plain)", "category": proteins, "calories": 59, "protein": 10.0, "carbs": 3.6, "fats": 0.4, "fiber": 0.0},
            {"name": "Eggs (whole)", "category": proteins, "calories": 155, "protein": 13.0, "carbs": 1.1, "fats": 11.0, "fiber": 0.0},
            {"name": "Tofu (firm)", "category": proteins, "calories": 76, "protein": 8.0, "carbs": 1.9, "fats": 4.8, "fiber": 0.6},
            {"name": "Lean Beef", "category": proteins, "calories": 250, "protein": 26.0, "carbs": 0.0, "fats": 15.0, "fiber": 0.0},
            
            # Vegetables (per 100g)
            {"name": "Broccoli", "category": vegetables, "calories": 34, "protein": 2.8, "carbs": 7.0, "fats": 0.4, "fiber": 2.6},
            {"name": "Spinach", "category": vegetables, "calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "fiber": 2.2},
            {"name": "Bell Peppers", "category": vegetables, "calories": 31, "protein": 1.0, "carbs": 7.0, "fats": 0.3, "fiber": 2.5},
            {"name": "Carrots", "category": vegetables, "calories": 41, "protein": 0.9, "carbs": 10.0, "fats": 0.2, "fiber": 2.8},
            {"name": "Cucumber", "category": vegetables, "calories": 16, "protein": 0.7, "carbs": 4.0, "fats": 0.1, "fiber": 0.5},
            {"name": "Tomatoes", "category": vegetables, "calories": 18, "protein": 0.9, "carbs": 3.9, "fats": 0.2, "fiber": 1.2},
            
            # Fruits
            {"name": "Apple (with skin)", "category": fruits, "calories": 52, "protein": 0.3, "carbs": 14.0, "fats": 0.2, "fiber": 2.4},
            {"name": "Banana", "category": fruits, "calories": 89, "protein": 1.1, "carbs": 23.0, "fats": 0.3, "fiber": 2.6},
            {"name": "Blueberries", "category": fruits, "calories": 57, "protein": 0.7, "carbs": 14.0, "fats": 0.3, "fiber": 2.4},
            
            # ...........................
        ]
        
        for food_data in foods_data:
            food, created = Food.objects.get_or_create(
                name=food_data["name"],
                defaults=food_data
            )
            if created:
                self.stdout.write(f"  + Added: {food.name}")
