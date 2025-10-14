from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'nutrition'
urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='nutrition:login'), name='logout'),
    
    
    # Main pages
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # meal plans
    path('meal-plan/<int:plan_id>/', views.meal_plan_detail, name='meal_plan_detail'),
    path('date/<str:date_str>/', views.meal_plan_by_date, name='meal_plan_by_date'),
    path('weekly/', views.weekly_view, name='weekly_view'),
    path('copy_day/<str:date_str>/', views.copy_day, name='copy_day'),
    path('analytics/', views.nutrition_analytics, name='nutrition_analytics'),

    # food management
    path('food/search/', views.food_search, name='food_search'),
    path('food/add-custom/', views.add_custom_food, name='add_custom_food'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('food/<int:food_id>/quick-add/', views.quick_add_food, name='quick_add_food'),

  # Meal entries
    path('meal-entry/add/<int:meal_plan_id>/', views.add_meal_entry, name='add_meal_entry'),
    path('meal-entry/add/<int:meal_plan_id>/<str:meal_type>/', views.add_meal_entry, name='add_meal_entry'),
    path('meal-entry/edit/<int:entry_id>/', views.edit_meal_entry, name='edit_meal_entry'), 
    path('meal-entry/delete/<int:entry_id>/', views.delete_meal_entry, name='delete_meal_entry'),
    
    
    # Recipes
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/add-to-meal/', views.add_recipe_to_meal, name='add_recipe_to_meal'),
    
    # Quick actions
    path('copy-yesterday/', views.copy_yesterday, name='copy_yesterday'),

  # about ;
  
   path('about/', views.about_developer, name='about_developer'),




]
