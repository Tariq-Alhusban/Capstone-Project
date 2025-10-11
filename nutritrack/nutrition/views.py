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
