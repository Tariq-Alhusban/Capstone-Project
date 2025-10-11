from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import MealPlan, Food, FoodCategory

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
    from datetime import date
    today = date.today()
    
    # Get or create today's meal plan
    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'goal_calories': 2000}
    )
    
    context = {
        'meal_plan': meal_plan,
        'total_foods': Food.objects.count(),
        'food_categories': FoodCategory.objects.all(),
        'recent_plans': MealPlan.objects.filter(user=request.user)[:5]
    }
    return render(request, 'nutrition/dashboard.html', context)