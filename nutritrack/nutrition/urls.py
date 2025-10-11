from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'nutrition'
urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='nutrition:login'), name='logout'),
    
    # Main pages
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('copy-yesterday/', views.copy_yesterday, name='copy_yesterday'),
    path('meal-plan/<int:plan_id>/', views.meal_plan_detail, name='meal_plan_detail'),
    path('meal-entry/add/<int:meal_plan_id>/<str:meal_type>/', views.add_meal_entry, name='add_meal_entry'),
    path('food/search/', views.food_search, name='food_search'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
]
