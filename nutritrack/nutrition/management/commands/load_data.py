from django.core.management.base import BaseCommand
from nutrition.models import FoodCategory, Food, MealPlan, MealEntry, RecipeTemplate, RecipeIngredient
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = '🚀 MEGA DATA LOADER - Load comprehensive sample data for NutriTrack app'

    def handle(self, *args, **options):
        """
        🚀 MEGA DATA LOADER for NutriTrack
        Loads comprehensive sample data including:
        - Demo users with different profiles (4 users)
        - Extensive food database (100+ foods)
        - Food categories with icons (15 categories)
        - Sample meal plans (30 days worth)
        - Complete recipe library (15+ recipes)
        - Realistic meal entries with variety
        """
        
        self.stdout.write("🔥 Starting MEGA DATA LOAD...")
        self.stdout.write("="*60)
        
        # ===========================================
        # 1. CREATE DEMO USERS
        # ===========================================
        self.stdout.write("👥 Creating demo users...")
        
        users_data = [
            {
                'username': 'ahmad_nutrition',
                'email': 'ahmad@example.com',
                'first_name': 'Ahmad',
                'last_name': 'Jouza',
                'goal_calories': 2200
            },
            {
                'username': 'sara_health',
                'email': 'sara@example.com', 
                'first_name': 'Sara',
                'last_name': 'Ali',
                'goal_calories': 1800
            },
            {
                'username': 'fitness_mike',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Fitness',
                'goal_calories': 2800
            },
            {
                'username': 'healthy_layla',
                'email': 'layla@example.com',
                'first_name': 'Layla',
                'last_name': 'Health',
                'goal_calories': 1600
            }
        ]
        
        user_objects = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            user_objects[user_data['username']] = user
            if created:
                self.stdout.write(f"  ✅ Created user: {user.first_name} {user.last_name}")
        
        # ===========================================
        # 2. CREATE FOOD CATEGORIES
        # ===========================================
        self.stdout.write("\n🏷️ Creating food categories...")
        
        categories_data = [
            ("🍖", "Proteins"),
            ("🥬", "Vegetables"), 
            ("🍎", "Fruits"),
            ("🍞", "Grains & Starches"),
            ("🥛", "Dairy Products"),
            ("🥑", "Healthy Fats & Oils"),
            ("🥜", "Nuts & Seeds"),
            ("🍰", "Desserts & Sweets"),
            ("🥤", "Beverages"),
            ("🌶️", "Spices & Seasonings"),
            ("🍲", "Middle Eastern"),
            ("🍝", "International"),
            ("🥗", "Salads & Dressings"),
            ("🍕", "Fast Food"),
            ("🧈", "Condiments")
        ]
        
        category_objects = {}
        for icon, name in categories_data:
            category, created = FoodCategory.objects.get_or_create(
                name=name,
                defaults={'icon': icon}
            )
            category_objects[name] = category
            if created:
                self.stdout.write(f"  ✅ Created category: {icon} {name}")

        # ===========================================
        # 3. CREATE COMPREHENSIVE FOOD DATABASE
        # ===========================================
        self.stdout.write(f"\n🍽️ Loading comprehensive food database...")
        
        # MEGA FOOD DATABASE (100+ foods with accurate nutrition data per 100g)
        foods_data = [
            # PROTEINS (per 100g)
            ("Chicken Breast (skinless)", "Proteins", 165, 31.0, 0.0, 3.6, 0.0, 74),
            ("Chicken Thigh (skinless)", "Proteins", 209, 26.0, 0.0, 11.0, 0.0, 77),
            ("Ground Chicken (lean)", "Proteins", 143, 25.0, 0.0, 4.5, 0.0, 81),
            ("Turkey Breast", "Proteins", 135, 30.0, 0.0, 1.0, 0.0, 70),
            ("Salmon Fillet", "Proteins", 208, 25.4, 0.0, 12.4, 0.0, 93),
            ("Tuna (canned in water)", "Proteins", 132, 28.0, 0.0, 1.3, 0.0, 107),
            ("Cod Fillet", "Proteins", 105, 23.0, 0.0, 0.9, 0.0, 78),
            ("Shrimp", "Proteins", 106, 20.0, 1.0, 1.7, 0.0, 111),
            ("Eggs (whole)", "Proteins", 155, 13.0, 1.1, 11.0, 0.0, 124),
            ("Egg Whites", "Proteins", 52, 11.0, 0.7, 0.2, 0.0, 166),
            ("Greek Yogurt (plain)", "Proteins", 59, 10.0, 3.6, 0.4, 0.0, 36),
            ("Cottage Cheese (low-fat)", "Proteins", 72, 12.0, 4.0, 1.0, 0.0, 405),
            ("Lean Beef (sirloin)", "Proteins", 158, 26.0, 0.0, 5.4, 0.0, 54),
            ("Ground Beef (93/7)", "Proteins", 152, 22.0, 0.0, 7.0, 0.0, 75),
            ("Tofu (firm)", "Proteins", 76, 8.0, 1.9, 4.8, 0.6, 7),
            ("Tempeh", "Proteins", 193, 19.0, 9.0, 11.0, 9.0, 9),
            ("Black Beans (cooked)", "Proteins", 132, 8.9, 23.0, 0.5, 8.7, 2),
            ("Lentils (cooked)", "Proteins", 116, 9.0, 20.0, 0.4, 7.9, 2),
            ("Chickpeas (cooked)", "Proteins", 164, 8.9, 27.0, 2.6, 7.6, 7),
            ("Whey Protein Powder", "Proteins", 400, 80.0, 5.0, 5.0, 0.0, 50),
            
            # VEGETABLES (per 100g)
            ("Broccoli", "Vegetables", 34, 2.8, 7.0, 0.4, 2.6, 33),
            ("Cauliflower", "Vegetables", 25, 1.9, 5.0, 0.3, 2.0, 15),
            ("Spinach (fresh)", "Vegetables", 23, 2.9, 3.6, 0.4, 2.2, 79),
            ("Kale", "Vegetables", 49, 4.3, 9.0, 0.9, 3.6, 38),
            ("Bell Peppers (red)", "Vegetables", 31, 1.0, 7.0, 0.3, 2.5, 4),
            ("Bell Peppers (green)", "Vegetables", 28, 1.0, 6.0, 0.2, 2.0, 3),
            ("Carrots", "Vegetables", 41, 0.9, 10.0, 0.2, 2.8, 69),
            ("Cucumber", "Vegetables", 16, 0.7, 4.0, 0.1, 0.5, 2),
            ("Tomatoes", "Vegetables", 18, 0.9, 3.9, 0.2, 1.2, 5),
            ("Cherry Tomatoes", "Vegetables", 18, 0.9, 3.9, 0.2, 1.2, 5),
            ("Zucchini", "Vegetables", 17, 1.2, 3.1, 0.3, 1.0, 8),
            ("Eggplant", "Vegetables", 25, 1.0, 6.0, 0.2, 3.0, 2),
            ("Onions", "Vegetables", 40, 1.1, 9.3, 0.1, 1.7, 4),
            ("Garlic", "Vegetables", 149, 6.4, 33.0, 0.5, 2.1, 17),
            ("Mushrooms (button)", "Vegetables", 22, 3.1, 3.3, 0.3, 1.0, 5),
            ("Asparagus", "Vegetables", 20, 2.2, 3.9, 0.1, 2.1, 2),
            ("Green Beans", "Vegetables", 31, 1.8, 7.0, 0.2, 2.7, 6),
            ("Sweet Potato", "Vegetables", 86, 1.6, 20.0, 0.1, 3.0, 5),
            ("Beets", "Vegetables", 43, 1.6, 10.0, 0.2, 2.8, 78),
            ("Cabbage", "Vegetables", 25, 1.3, 6.0, 0.1, 2.5, 18),
            
            # FRUITS (per 100g)
            ("Apple (with skin)", "Fruits", 52, 0.3, 14.0, 0.2, 2.4, 1),
            ("Banana", "Fruits", 89, 1.1, 23.0, 0.3, 2.6, 1),
            ("Orange", "Fruits", 47, 0.9, 12.0, 0.1, 2.4, 0),
            ("Strawberries", "Fruits", 32, 0.7, 8.0, 0.3, 2.0, 1),
            ("Blueberries", "Fruits", 57, 0.7, 14.0, 0.3, 2.4, 1),
            ("Raspberries", "Fruits", 52, 1.2, 12.0, 0.7, 6.5, 1),
            ("Grapes", "Fruits", 62, 0.6, 16.0, 0.2, 0.9, 2),
            ("Pineapple", "Fruits", 50, 0.5, 13.0, 0.1, 1.4, 1),
            ("Mango", "Fruits", 60, 0.8, 15.0, 0.4, 1.6, 1),
            ("Avocado", "Fruits", 160, 2.0, 9.0, 15.0, 7.0, 7),
            ("Watermelon", "Fruits", 30, 0.6, 8.0, 0.2, 0.4, 1),
            ("Cantaloupe", "Fruits", 34, 0.8, 8.0, 0.2, 0.9, 16),
            ("Kiwi", "Fruits", 61, 1.1, 15.0, 0.5, 3.0, 3),
            ("Peach", "Fruits", 39, 0.9, 10.0, 0.3, 1.5, 0),
            ("Pear", "Fruits", 57, 0.4, 15.0, 0.1, 3.1, 1),
            ("Lemon", "Fruits", 29, 1.1, 9.0, 0.3, 2.8, 2),
            
            # GRAINS & STARCHES (per 100g, cooked unless specified)
            ("Brown Rice (cooked)", "Grains & Starches", 123, 2.6, 25.0, 1.0, 1.8, 5),
            ("White Rice (cooked)", "Grains & Starches", 130, 2.4, 28.0, 0.3, 0.4, 5),
            ("Quinoa (cooked)", "Grains & Starches", 120, 4.4, 22.0, 1.9, 2.8, 5),
            ("Oats (dry)", "Grains & Starches", 389, 16.9, 66.0, 6.9, 10.0, 2),
            ("Oatmeal (cooked)", "Grains & Starches", 68, 2.4, 12.0, 1.4, 1.7, 3),
            ("Whole Wheat Bread", "Grains & Starches", 247, 13.0, 41.0, 4.2, 7.0, 550),
            ("White Bread", "Grains & Starches", 265, 9.0, 49.0, 3.2, 2.7, 491),
            ("Pasta (whole wheat, cooked)", "Grains & Starches", 124, 5.3, 25.0, 1.1, 3.9, 3),
            ("Pasta (white, cooked)", "Grains & Starches", 131, 5.0, 25.0, 1.1, 1.8, 1),
            ("Sweet Potato (baked)", "Grains & Starches", 90, 2.0, 21.0, 0.2, 3.3, 6),
            ("Regular Potato (baked)", "Grains & Starches", 93, 2.5, 21.0, 0.1, 2.2, 7),
            ("Barley (cooked)", "Grains & Starches", 123, 2.3, 28.0, 0.4, 3.8, 3),
            
            # DAIRY PRODUCTS (per 100g)
            ("Milk (whole)", "Dairy Products", 61, 3.2, 4.8, 3.3, 0.0, 44),
            ("Milk (2%)", "Dairy Products", 50, 3.3, 4.8, 1.9, 0.0, 44),
            ("Milk (skim)", "Dairy Products", 34, 3.4, 5.0, 0.2, 0.0, 44),
            ("Cheddar Cheese", "Dairy Products", 403, 25.0, 1.3, 33.0, 0.0, 653),
            ("Mozzarella Cheese", "Dairy Products", 300, 22.0, 2.2, 22.0, 0.0, 627),
            ("Regular Yogurt", "Dairy Products", 61, 3.5, 4.7, 3.3, 0.0, 46),
            ("Butter", "Dairy Products", 717, 0.9, 0.1, 81.0, 0.0, 643),
            ("Cream Cheese", "Dairy Products", 342, 6.0, 4.1, 34.0, 0.0, 321),
            
            # HEALTHY FATS & OILS (per 100g)
            ("Olive Oil (extra virgin)", "Healthy Fats & Oils", 884, 0.0, 0.0, 100.0, 0.0, 2),
            ("Coconut Oil", "Healthy Fats & Oils", 862, 0.0, 0.0, 100.0, 0.0, 0),
            ("Avocado Oil", "Healthy Fats & Oils", 884, 0.0, 0.0, 100.0, 0.0, 0),
            
            # NUTS & SEEDS (per 100g)
            ("Almonds", "Nuts & Seeds", 579, 21.0, 22.0, 50.0, 12.0, 1),
            ("Walnuts", "Nuts & Seeds", 654, 15.0, 14.0, 65.0, 6.7, 2),
            ("Cashews", "Nuts & Seeds", 553, 18.0, 30.0, 44.0, 3.3, 12),
            ("Peanuts", "Nuts & Seeds", 567, 26.0, 16.0, 49.0, 8.5, 18),
            ("Peanut Butter", "Nuts & Seeds", 588, 25.0, 20.0, 50.0, 8.0, 476),
            ("Almond Butter", "Nuts & Seeds", 614, 21.0, 19.0, 56.0, 10.0, 1),
            ("Chia Seeds", "Nuts & Seeds", 486, 17.0, 42.0, 31.0, 34.0, 16),
            ("Flax Seeds", "Nuts & Seeds", 534, 18.0, 29.0, 42.0, 27.0, 30),
            ("Sunflower Seeds", "Nuts & Seeds", 584, 21.0, 20.0, 51.0, 8.6, 9),
            ("Pumpkin Seeds", "Nuts & Seeds", 559, 19.0, 54.0, 19.0, 18.0, 7),
            
            # MIDDLE EASTERN FOODS (per 100g)
            ("Hummus", "Middle Eastern", 177, 8.0, 20.0, 8.0, 6.0, 379),
            ("Falafel", "Middle Eastern", 333, 13.0, 32.0, 18.0, 4.0, 294),
            ("Tabbouleh", "Middle Eastern", 36, 1.5, 7.0, 0.9, 2.0, 15),
            ("Baba Ganoush", "Middle Eastern", 150, 3.0, 8.0, 13.0, 4.0, 296),
            ("Pita Bread", "Middle Eastern", 275, 9.0, 56.0, 1.2, 2.0, 536),
            ("Labneh", "Middle Eastern", 83, 6.0, 5.0, 5.0, 0.0, 85),
            ("Tahini", "Middle Eastern", 595, 18.0, 18.0, 54.0, 5.0, 115),
            ("Za'atar", "Middle Eastern", 279, 5.0, 44.0, 10.0, 18.0, 2840),
            ("Fattoush Salad", "Middle Eastern", 95, 2.5, 8.0, 6.5, 3.0, 180),
            ("Kibbeh", "Middle Eastern", 195, 12.0, 15.0, 10.0, 2.0, 425),
            
            # BEVERAGES (per 100ml)
            ("Water", "Beverages", 0, 0.0, 0.0, 0.0, 0.0, 0),
            ("Green Tea", "Beverages", 1, 0.0, 0.0, 0.0, 0.0, 1),
            ("Black Coffee", "Beverages", 2, 0.3, 0.0, 0.0, 0.0, 2),
            ("Almond Milk (unsweetened)", "Beverages", 15, 0.6, 0.6, 1.2, 0.4, 69),
            ("Coconut Milk", "Beverages", 19, 0.2, 1.8, 1.6, 0.0, 13),
            ("Orange Juice", "Beverages", 45, 0.7, 10.0, 0.2, 0.2, 1),
            ("Apple Juice", "Beverages", 46, 0.1, 11.0, 0.1, 0.1, 2),
            
            # DESSERTS & SWEETS (per 100g)
            ("Dark Chocolate (70%)", "Desserts & Sweets", 598, 8.0, 46.0, 43.0, 11.0, 6),
            ("Milk Chocolate", "Desserts & Sweets", 535, 8.0, 59.0, 30.0, 3.0, 79),
            ("Vanilla Ice Cream", "Desserts & Sweets", 207, 3.5, 24.0, 11.0, 0.7, 80),
            ("Cookies (chocolate chip)", "Desserts & Sweets", 488, 5.0, 68.0, 21.0, 2.0, 386),
            ("Honey", "Desserts & Sweets", 304, 0.3, 82.0, 0.0, 0.2, 4),
            
            # FAST FOOD (per 100g)
            ("French Fries", "Fast Food", 365, 4.0, 63.0, 17.0, 3.8, 246),
            ("Burger (beef)", "Fast Food", 295, 17.0, 23.0, 17.0, 2.0, 497),
            ("Pizza (cheese)", "Fast Food", 266, 12.0, 33.0, 10.0, 2.3, 598),
            ("Fried Chicken", "Fast Food", 320, 19.0, 8.0, 24.0, 0.0, 540),
            
            # CONDIMENTS (per 100g)
            ("Ketchup", "Condiments", 112, 1.0, 25.0, 0.1, 0.0, 907),
            ("Mustard", "Condiments", 60, 3.7, 5.8, 3.3, 3.0, 1135),
            ("Mayonnaise", "Condiments", 680, 1.0, 0.6, 75.0, 0.0, 435),
            ("Hot Sauce", "Condiments", 12, 0.9, 1.0, 0.8, 1.4, 1172),
            
            # INTERNATIONAL (per 100g)
            ("Sushi Rice", "International", 130, 2.4, 28.0, 0.3, 0.4, 5),
            ("Pasta Sauce (marinara)", "International", 29, 1.6, 7.0, 0.2, 1.4, 431)
        ]
        
        food_objects = {}
        foods_count = 0
        for name, category_name, calories, protein, carbs, fats, fiber, sodium in foods_data:
            food, created = Food.objects.get_or_create(
                name=name,
                defaults={
                    'category': category_objects[category_name],
                    'calories': calories,
                    'protein': protein,
                    'carbs': carbs,
                    'fats': fats,
                    'fiber': fiber,
                    'sodium': sodium
                }
            )
            food_objects[name] = food
            if created:
                foods_count += 1
                if foods_count % 20 == 0:
                    self.stdout.write(f"  ✅ Loaded {foods_count} foods...")
        
        self.stdout.write(f"  🎉 Total foods loaded: {foods_count}")

        # ===========================================
        # 4. CREATE SAMPLE RECIPES
        # ===========================================
        self.stdout.write(f"\n👩‍🍳 Creating sample recipes...")
        
        recipes_data = [
            {
                'name': 'Power Protein Smoothie',
                'description': 'High-protein breakfast smoothie perfect for workouts',
                'user': 'ahmad_nutrition',
                'ingredients': [
                    ('Greek Yogurt (plain)', 200, 'g'),
                    ('Banana', 100, 'g'),
                    ('Peanut Butter', 20, 'g'),
                    ('Milk (2%)', 150, 'ml'),
                    ('Whey Protein Powder', 25, 'g')
                ]
            },
            {
                'name': 'Mediterranean Bowl',
                'description': 'Healthy Mediterranean-style protein bowl',
                'user': 'sara_health',
                'ingredients': [
                    ('Quinoa (cooked)', 80, 'g'),
                    ('Hummus', 50, 'g'),
                    ('Tabbouleh', 100, 'g'),
                    ('Falafel', 80, 'g'),
                    ('Cucumber', 50, 'g'),
                    ('Cherry Tomatoes', 60, 'g')
                ]
            },
            {
                'name': 'Healthy Breakfast Bowl',
                'description': 'Nutritious morning meal with oats and fruits',
                'user': 'healthy_layla',
                'ingredients': [
                    ('Oatmeal (cooked)', 150, 'g'),
                    ('Blueberries', 60, 'g'),
                    ('Almonds', 20, 'g'),
                    ('Chia Seeds', 10, 'g'),
                    ('Honey', 15, 'g'),
                    ('Greek Yogurt (plain)', 100, 'g')
                ]
            },
            {
                'name': 'Grilled Chicken Salad',
                'description': 'Fresh and filling protein-packed salad',
                'user': 'fitness_mike',
                'ingredients': [
                    ('Chicken Breast (skinless)', 120, 'g'),
                    ('Spinach (fresh)', 80, 'g'),
                    ('Cherry Tomatoes', 60, 'g'),
                    ('Cucumber', 50, 'g'),
                    ('Bell Peppers (red)', 40, 'g'),
                    ('Olive Oil (extra virgin)', 10, 'ml'),
                    ('Avocado', 50, 'g')
                ]
            },
            {
                'name': 'Post-Workout Recovery Smoothie',
                'description': 'Perfect blend for muscle recovery',
                'user': 'fitness_mike',
                'ingredients': [
                    ('Whey Protein Powder', 30, 'g'),
                    ('Banana', 120, 'g'),
                    ('Peanut Butter', 15, 'g'),
                    ('Milk (skim)', 200, 'ml'),
                    ('Oats (dry)', 25, 'g')
                ]
            },
            {
                'name': 'Healthy Avocado Toast',
                'description': 'Simple and nutritious breakfast option',
                'user': 'sara_health',
                'ingredients': [
                    ('Whole Wheat Bread', 60, 'g'),
                    ('Avocado', 80, 'g'),
                    ('Eggs (whole)', 100, 'g'),
                    ('Cherry Tomatoes', 40, 'g'),
                    ('Spinach (fresh)', 20, 'g')
                ]
            },
            {
                'name': 'Quinoa Veggie Bowl',
                'description': 'Colorful vegetarian protein bowl',
                'user': 'healthy_layla',
                'ingredients': [
                    ('Quinoa (cooked)', 100, 'g'),
                    ('Broccoli', 80, 'g'),
                    ('Sweet Potato (baked)', 100, 'g'),
                    ('Chickpeas (cooked)', 60, 'g'),
                    ('Tahini', 15, 'g'),
                    ('Kale', 40, 'g')
                ]
            },
            {
                'name': 'Salmon & Brown Rice',
                'description': 'Omega-3 rich dinner with complex carbs',
                'user': 'ahmad_nutrition',
                'ingredients': [
                    ('Salmon Fillet', 120, 'g'),
                    ('Brown Rice (cooked)', 100, 'g'),
                    ('Asparagus', 100, 'g'),
                    ('Olive Oil (extra virgin)', 8, 'ml'),
                    ('Lemon', 20, 'g')
                ]
            },
            {
                'name': 'Energy Nut Mix',
                'description': 'Perfect snack for sustained energy',
                'user': 'fitness_mike',
                'ingredients': [
                    ('Almonds', 20, 'g'),
                    ('Walnuts', 15, 'g'),
                    ('Pumpkin Seeds', 10, 'g'),
                    ('Dark Chocolate (70%)', 15, 'g')
                ]
            },
            {
                'name': 'Green Detox Smoothie',
                'description': 'Nutrient-packed green smoothie',
                'user': 'healthy_layla',
                'ingredients': [
                    ('Spinach (fresh)', 60, 'g'),
                    ('Kale', 40, 'g'),
                    ('Apple (with skin)', 100, 'g'),
                    ('Banana', 80, 'g'),
                    ('Chia Seeds', 10, 'g'),
                    ('Almond Milk (unsweetened)', 200, 'ml')
                ]
            },
            {
                'name': 'Middle Eastern Platter',
                'description': 'Traditional Middle Eastern mezze',
                'user': 'ahmad_nutrition',
                'ingredients': [
                    ('Hummus', 60, 'g'),
                    ('Falafel', 100, 'g'),
                    ('Pita Bread', 80, 'g'),
                    ('Baba Ganoush', 40, 'g'),
                    ('Tabbouleh', 80, 'g'),
                    ('Labneh', 50, 'g')
                ]
            },
            {
                'name': 'Protein-Packed Omelette',
                'description': 'High-protein breakfast with vegetables',
                'user': 'sara_health',
                'ingredients': [
                    ('Eggs (whole)', 150, 'g'),
                    ('Egg Whites', 100, 'g'),
                    ('Spinach (fresh)', 50, 'g'),
                    ('Mushrooms (button)', 60, 'g'),
                    ('Bell Peppers (green)', 40, 'g'),
                    ('Cheddar Cheese', 30, 'g')
                ]
            },
            {
                'name': 'Recovery Rice Bowl',
                'description': 'Post-training carb and protein combination',
                'user': 'fitness_mike',
                'ingredients': [
                    ('Brown Rice (cooked)', 120, 'g'),
                    ('Chicken Thigh (skinless)', 100, 'g'),
                    ('Sweet Potato (baked)', 80, 'g'),
                    ('Broccoli', 60, 'g'),
                    ('Avocado', 40, 'g')
                ]
            },
            {
                'name': 'Antioxidant Berry Bowl',
                'description': 'Superfood bowl packed with antioxidants',
                'user': 'healthy_layla',
                'ingredients': [
                    ('Greek Yogurt (plain)', 150, 'g'),
                    ('Blueberries', 60, 'g'),
                    ('Strawberries', 50, 'g'),
                    ('Raspberries', 40, 'g'),
                    ('Almonds', 20, 'g'),
                    ('Flax Seeds', 10, 'g'),
                    ('Honey', 15, 'g')
                ]
            },
            {
                'name': 'Healthy Tuna Salad',
                'description': 'Light and refreshing protein salad',
                'user': 'sara_health',
                'ingredients': [
                    ('Tuna (canned in water)', 100, 'g'),
                    ('Spinach (fresh)', 80, 'g'),
                    ('Cherry Tomatoes', 60, 'g'),
                    ('Cucumber', 50, 'g'),
                    ('Olive Oil (extra virgin)', 8, 'ml'),
                    ('Lemon', 15, 'g'),
                    ('Avocado', 60, 'g')
                ]
            }
        ]
        
        recipe_objects = {}
        recipes_count = 0
        for recipe_data in recipes_data:
            user = user_objects[recipe_data['user']]
            recipe, created = RecipeTemplate.objects.get_or_create(
                user=user,
                name=recipe_data['name'],
                defaults={'description': recipe_data['description']}
            )
            
            if created:
                recipes_count += 1
                self.stdout.write(f"  ✅ Created recipe: {recipe.name}")
                
                # Add ingredients
                for food_name, quantity, unit in recipe_data['ingredients']:
                    if food_name in food_objects:
                        RecipeIngredient.objects.get_or_create(
                            recipe=recipe,
                            food=food_objects[food_name],
                            defaults={'quantity': quantity, 'unit': unit}
                        )
                
                recipe_objects[recipe_data['name']] = recipe
        
        self.stdout.write(f"  🎉 Total recipes created: {recipes_count}")

        # ===========================================
        # 5. CREATE REALISTIC MEAL PLANS & ENTRIES
        # ===========================================
        self.stdout.write(f"\n📅 Creating comprehensive meal plans (30 days)...")
        
        # Create meal plans for the last 30 days for multiple users
        today = date.today()
        meal_plans_count = 0
        meal_entries_count = 0
        
        # Define realistic meal patterns for different users
        meal_patterns = {
            'ahmad_nutrition': {
                'goal_calories': 2200,
                'favorite_foods': ['Chicken Breast (skinless)', 'Brown Rice (cooked)', 'Greek Yogurt (plain)', 'Almonds', 'Banana']
            },
            'sara_health': {
                'goal_calories': 1800,
                'favorite_foods': ['Salmon Fillet', 'Quinoa (cooked)', 'Avocado', 'Spinach (fresh)', 'Blueberries']
            },
            'fitness_mike': {
                'goal_calories': 2800,
                'favorite_foods': ['Lean Beef (sirloin)', 'Sweet Potato (baked)', 'Whey Protein Powder', 'Peanut Butter', 'Oatmeal (cooked)']
            },
            'healthy_layla': {
                'goal_calories': 1600,
                'favorite_foods': ['Tofu (firm)', 'Chickpeas (cooked)', 'Kale', 'Chia Seeds', 'Apple (with skin)']
            }
        }
        
        # Create meal plans for each user for the last 30 days
        for days_back in range(30):
            meal_date = today - timedelta(days=days_back)
            
            # Skip some days randomly to make it more realistic (not everyone logs every day)
            if random.random() < 0.15:  # 15% chance to skip a day
                continue
                
            for username, pattern in meal_patterns.items():
                user = user_objects[username]
                
                # Create meal plan
                meal_plan, created = MealPlan.objects.get_or_create(
                    user=user,
                    date=meal_date,
                    defaults={
                        'goal_calories': pattern['goal_calories'],
                        'notes': f'Day {31-days_back} - {meal_date.strftime("%A")}'
                    }
                )
                
                if created:
                    meal_plans_count += 1
                    
                    # Create meal entries for this day
                    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
                    
                    for meal_type in meal_types:
                        # Skip some meals randomly to make it realistic
                        if random.random() < 0.1:  # 10% chance to skip a meal
                            continue
                        
                        # Select 2-3 foods for this meal
                        num_foods = random.randint(2, 3)
                        selected_foods = random.sample(pattern['favorite_foods'], min(num_foods, len(pattern['favorite_foods'])))
                        
                        for food_name in selected_foods:
                            if food_name in food_objects:
                                food = food_objects[food_name]
                                
                                # Calculate reasonable quantity
                                if meal_type == 'breakfast':
                                    quantity = random.randint(80, 150)
                                elif meal_type in ['lunch', 'dinner']:
                                    quantity = random.randint(100, 200)
                                else:  # snack
                                    quantity = random.randint(30, 80)
                                
                                # Determine appropriate unit
                                unit = 'ml' if food.category.name == 'Beverages' else 'g'
                                
                                MealEntry.objects.get_or_create(
                                    meal_plan=meal_plan,
                                    food=food,
                                    meal_type=meal_type,
                                    defaults={
                                        'quantity': quantity,
                                        'unit': unit
                                    }
                                )
                                meal_entries_count += 1
        
        self.stdout.write(f"  ✅ Created {meal_plans_count} meal plans")
        self.stdout.write(f"  ✅ Created {meal_entries_count} meal entries")

        # ===========================================
        # 6. FINAL SUMMARY
        # ===========================================
        self.stdout.write(f"\n" + "="*60)
        self.stdout.write(f"🎉 MEGA DATA LOAD COMPLETE!")
        self.stdout.write(f"="*60)
        self.stdout.write(f"👥 Users created: {len(users_data)}")
        self.stdout.write(f"🏷️ Categories created: {len(categories_data)}")
        self.stdout.write(f"🍽️ Foods loaded: {foods_count}")
        self.stdout.write(f"👩‍🍳 Recipes created: {recipes_count}")
        self.stdout.write(f"📅 Meal plans created: {meal_plans_count}")
        self.stdout.write(f"🍽️ Meal entries created: {meal_entries_count}")
        self.stdout.write(f"="*60)
        
        self.stdout.write(f"\n🚀 READY FOR DEMO!")
        self.stdout.write(f"✅ Your app now has realistic data spanning 30 days")
        self.stdout.write(f"✅ Multiple users with different eating patterns")
        self.stdout.write(f"✅ Comprehensive food database with accurate nutrition")
        self.stdout.write(f"✅ Variety of recipes from different cuisines")
        self.stdout.write(f"✅ Analytics will show meaningful trends and insights")
        
        self.stdout.write(f"\n📊 TEST YOUR ANALYTICS:")
        self.stdout.write(f"• Visit /analytics/ to see comprehensive 30-day insights")
        self.stdout.write(f"• Check /weekly/ for weekly progress views")  
        self.stdout.write(f"• Try different user accounts to see varied data")
        
        self.stdout.write(f"\n🎯 FOR YOUR PRESENTATION:")
        self.stdout.write(f"• Show the dashboard with today's meals")
        self.stdout.write(f"• Demonstrate the analytics with real trend data")
        self.stdout.write(f"• Display the comprehensive food database")
        self.stdout.write(f"• Showcase recipe creation and management")
        self.stdout.write(f"• Highlight the mobile-responsive design")

        self.stdout.write(self.style.SUCCESS('\n🎯 MEGA DATA LOADING SUCCESSFUL!'))