from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import MealPlan, Food, FoodCategory
from django.db.models import Q
from datetime import date, timedelta


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/dashboard/'

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('nutrition:login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def dashboard(request):
    today = date.today()
    
    # Get or create today's meal plan
    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'goal_calories': 2000}
    )

    # Meal types for template
    meal_types = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snacks'),
    ]
    
    context = {
        'meal_plan': meal_plan,
        'meal_types': meal_types,
        'total_foods': Food.objects.count(),
        'food_categories': FoodCategory.objects.all(),
        'recent_plans': MealPlan.objects.filter(
            user=request.user
        ).exclude(date=today).order_by('-date')[:7]
    }
    return render(request, 'nutrition/dashboard.html', context)

@login_required
def copy_yesterday(request):
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    try:
        yesterday_plan = MealPlan.objects.get(user=request.user, date=yesterday)
        today_plan, created = MealPlan.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                'goal_calories': yesterday_plan.goal_calories,
                'notes': f"Copied from {yesterday}"
            }
        )
        
        # Copy meal entries
        for entry in yesterday_plan.mealentry_set.all():
            MealEntry.objects.get_or_create(
                meal_plan=today_plan,
                food=entry.food,
                meal_type=entry.meal_type,
                defaults={
                    'quantity': entry.quantity,
                    'unit': entry.unit
                }
            )
        
        messages.success(request, f"Copied {yesterday_plan.mealentry_set.count()} items from yesterday!")
        
    except MealPlan.DoesNotExist:
        messages.error(request, "No meal plan found for yesterday.")
    
    return redirect('nutrition:dashboard')

@login_required
def meal_plan_detail(request, plan_id):
    meal_plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)
    
    # Group entries by meal type
    entries_by_meal = {}
    for meal_type, display_name in [('breakfast', 'Breakfast'), ('lunch', 'Lunch'), 
                                   ('dinner', 'Dinner'), ('snack', 'Snacks')]:
        entries_by_meal[meal_type] = meal_plan.mealentry_set.filter(meal_type=meal_type)
    
    context = {
        'meal_plan': meal_plan,
        'entries_by_meal': entries_by_meal,
    }
    return render(request, 'nutrition/meal_plan_detail.html', context)

from django.core.paginator import Paginator

@login_required
def food_search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    foods = Food.objects.all()
    
    if query:
        foods = foods.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query)
        )
    
    if category:
        foods = foods.filter(category__name=category)
    
    # Pagination
    paginator = Paginator(foods, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'foods': page_obj,
        'query': query,
        'selected_category': category,
        'categories': FoodCategory.objects.all(),
        'total_results': foods.count(),
    }
    return render(request, 'nutrition/food_search.html', context)

@login_required
def add_custom_food(request):
    if request.method == 'POST':
        form = CustomFoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.is_custom = True
            food.created_by = request.user
            food.save()
            messages.success(request, f'Custom food "{food.name}" added successfully!')
            return redirect('nutrition:food_search')
    else:
        form = CustomFoodForm()
    
    context = {
        'form': form,
        'categories': FoodCategory.objects.all(),
    }
    return render(request, 'nutrition/add_custom_food.html', context)




from django.shortcuts import get_object_or_404  # automatically return a 404 error page if the object doesn’t exist.
from .forms import MealEntryForm


@login_required
def add_meal_entry(request, meal_plan_id, meal_type=None):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    
    if request.method == 'POST':
        form = MealEntryForm(request.POST)
        if form.is_valid():
            meal_entry = form.save(commit=False)
            meal_entry.meal_plan = meal_plan
            if meal_type:
                meal_entry.meal_type = meal_type
            meal_entry.save()
            
            messages.success(request, f'Added {meal_entry.food.name} to {meal_entry.get_meal_type_display()}!')
            return redirect('nutrition:dashboard')
    else:
        initial_data = {'meal_type': meal_type} if meal_type else {}
        form = MealEntryForm(initial=initial_data)
    
    context = {
        'form': form,
        'meal_plan': meal_plan,
        'meal_type': meal_type,
        'recent_foods': Food.objects.filter(
            mealentry__meal_plan__user=request.user
        ).distinct()[:10]
    }
    return render(request, 'nutrition/add_meal_entry.html', context)

@login_required
def quick_add_food(request, food_id):
    """Quick add food to today's meal plan"""
    food = get_object_or_404(Food, id=food_id)
    today = date.today()
    
    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'goal_calories': 2000}
    )
    
    if request.method == 'POST':
        meal_type = request.POST.get('meal_type', 'lunch')
        quantity = float(request.POST.get('quantity', 100))
        unit = request.POST.get('unit', 'g')
        
        MealEntry.objects.create(
            meal_plan=meal_plan,
            food=food,
            meal_type=meal_type,
            quantity=quantity,
            unit=unit
        )
        
        messages.success(request, f'Added {food.name} to {meal_type}!')
        return redirect('nutrition:dashboard')
    
    context = {
        'food': food,
        'meal_plan': meal_plan,
    }
    return render(request, 'nutrition/quick_add_food.html', context)

@login_required
def edit_meal_entry(request, entry_id):
    entry = get_object_or_404(MealEntry, id=entry_id, meal_plan__user=request.user)
    
    if request.method == 'POST':
        form = MealEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {entry.food.name}!')
            return redirect('nutrition:dashboard')
    else:
        form = MealEntryForm(instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'is_edit': True,
    }
    return render(request, 'nutrition/add_meal_entry.html', context)

@login_required
def delete_meal_entry(request, entry_id):
    entry = get_object_or_404(MealEntry, id=entry_id, meal_plan__user=request.user)
    
    if request.method == 'POST':
        food_name = entry.food.name
        entry.delete()
        messages.success(request, f'Removed {food_name}!')
        return redirect('nutrition:dashboard')
    
    context = {'entry': entry}
    return render(request, 'nutrition/delete_meal_entry.html', context)

from .forms import RecipeTemplateForm, RecipeIngredientFormSet

@login_required
def my_recipes(request):
    recipes = RecipeTemplate.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'recipes': recipes,
        'total_recipes': recipes.count(),
    }
    return render(request, 'nutrition/my_recipes.html', context)

@login_required
def create_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeTemplateForm(request.POST)
        ingredient_formset = RecipeIngredientFormSet(request.POST)
        
        if recipe_form.is_valid() and ingredient_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            
            # Save ingredients
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            
            messages.success(request, f'Recipe "{recipe.name}" created successfully!')
            return redirect('nutrition:recipe_detail', recipe.id)
    else:
        recipe_form = RecipeTemplateForm()
        ingredient_formset = RecipeIngredientFormSet()
    
    context = {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'foods': Food.objects.all().order_by('category', 'name'),
    }
    return render(request, 'nutrition/create_recipe.html', context)

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(RecipeTemplate, id=recipe_id, user=request.user)
    ingredients = recipe.recipeingredient_set.all().select_related('food')
    
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'total_ingredients': ingredients.count(),
    }
    return render(request, 'nutrition/recipe_detail.html', context)

@login_required
def add_recipe_to_meal(request, recipe_id):
    """Add entire recipe to today's meal plan"""
    recipe = get_object_or_404(RecipeTemplate, id=recipe_id, user=request.user)
    today = date.today()
    
    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'goal_calories': 2000}
    )
    
    if request.method == 'POST':
        meal_type = request.POST.get('meal_type', 'lunch')
        
        # Add all recipe ingredients as separate meal entries
        added_count = 0
        for ingredient in recipe.recipeingredient_set.all():
            MealEntry.objects.create(
                meal_plan=meal_plan,
                food=ingredient.food,
                meal_type=meal_type,
                quantity=ingredient.quantity,
                unit=ingredient.unit
            )
            added_count += 1
        
        messages.success(request, f'Added recipe "{recipe.name}" ({added_count} ingredients) to {meal_type}!')
        return redirect('nutrition:dashboard')
    
    context = {
        'recipe': recipe,
        'meal_plan': meal_plan,
    }
    return render(request, 'nutrition/add_recipe_to_meal.html', context)
