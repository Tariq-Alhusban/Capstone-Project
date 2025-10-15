# 🍎 NutriTrack - Nutrition & Meal Planning App - Tariq Alhusban

![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.13.7-blue.svg)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)

> **NutriTrack** is a Django web application for daily nutrition tracking and meal planning. This capstone project demonstrates advanced Django development with M2M relationships, custom authentication, and mobile-responsive design.

 Users can create daily meal plans, log foods with macronutrient tracking, create reusable recipes, and view detailed nutritional summaries.

---


## Table of Contents

- [Features](#-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#-project-structure)
- [Data Model & Relationships & ERD](#-database-architecture-erd)
- [Development Roadmap](#-development-roadmap)
- [Sample Data Loaded](#-sample-data-loaded)
- [Installation Guide](#installation-guide)
- [User Stories](#user-stories)
- [Challenges Encountered & Solutions](#challenges-encountered--solutions)
- [Future Enhancements](#future-enhancements)
- [Security Considerations](#security-considerations)
- [Performance Optimizations](#performance-optimizations)
- [Testing Strategy](#testing-strategy)
- [Contributing](#contributing)
- [License](#license)


## 🎯 Features

### Core Functionality
- **User Authentication**: Secure registration, login, logout with personalized dashboards
- **Dashboard**: Daily meal overview with progress tracking and nutrition statistics
- 🍽️**Smart Meal Planning**: Add, edit, delete and Track breakfast, lunch, dinner, and snacks with automatic nutrition calculations
- 🔍**Advanced Food Database**: Searchable database with alot of foods with detailed nutritional information and custom food creation
- 📝**Recipe Management**: Create, Save and reuse custom recipes with multiple ingredients
- **Weekly Analytics**: Comprehensive weekly nutrition summaries and trends
- **Mobile Responsive**: Optimized for mobile devices with touch-friendly interactions

### Advanced Features
- **Custom Food Creation**: Add personal foods with nutritional data
- **Unit Conversion**: Support for grams, cups, tablespoons, pieces, and servings
- **Quick Actions**: Copy yesterday's meals, quick-add favorite foods
- 📊**Progress Tracking**: Visual progress bars and goal achievement indicators
- **Data Analytics**: 30-day nutrition analytics with trends and insights

### 🔄 CRUD Operations
- for Meals (Breakfast, Lunch, Dinner, etc.)
- or Food Items under each meal

## Tech Stack

### Backend
- **Framework**: Django 5.2.7
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Authentication**: Django's built-in User Authentication System
- **Admin Interface**: Django Admin with custom configurations

### Frontend
- **Templates**: HTML + Django Template Language (DTL)
- **Styling**: Custom CSS with responsive design
- **Layout**: CSS Grid and Flexbox
- **Scripts**: Vanilla JavaScript (Mobile interactions)


### Development Tools
- **Version Control**: Git & GitHub
- **Package Management**: pip & requirements.txt
- **Virtual Environment**: pipenv shell
- **Code Editor**: VS Code compatible


## 📁 Project Structure
```
Capstone-Project/
│
├── Pipfile
├── Pipfile.lock
├── README.md
│
└── nutritrack/
    ├── manage.py
    │
    ├── nutritrack/                    # Project settings folder
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── nutrition/                     # Main Django app
    │   ├── migrations/
    │   │   ├── __init__.py
    │   │   └── 0001_initial.py
    │   │
    │   ├── management/
    │   │   └── commands/
    │   │       ├── __init__.py
    │   │       └── load_data.py
    │   │
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── views.py
    │   └── urls.py
    │
    ├── static/
    │   ├── css/
    │   ├── images/
    │   └── js/
    │
    └── templates/
        ├── auth/
        └── nutrition/
```

### Directory Descriptions

- **Pipfile / Pipfile.lock** - Python dependencies management (Pipenv)
- **README.md** - Project documentation
- **nutritrack/** - Main project directory
- **manage.py** - Django management command-line utility
- **nutritrack/nutritrack/** - Project settings and configuration folder
- **nutritrack/nutrition/** - Main Django application with models, views, and templates
- **static/** - Static files (CSS, images, JavaScript)
- **templates/** - HTML templates organized by feature
  
## 🏗 Database Architecture (ERD)


```mermaid
erDiagram
    USER ||--o{ MEAL_PLAN : owns
    USER ||--o{ FOOD : "creates custom"
    
    FOOD_CATEGORY ||--o{ FOOD : categorizes
    MEAL_PLAN ||--o{ MEAL_ENTRY : contains
    FOOD ||--o{ MEAL_ENTRY : "used in"
    
    USER {
        int id PK
        string username
        string email
        datetime created_at
    }
    
    FOOD_CATEGORY {
        int id PK
        string name "Proteins, Vegetables, Fruits, etc"
        string icon "🥩, 🥬, 🍎, etc"
    }
    
    FOOD {
        int id PK
        string name
        int category_id FK
        int calories "per 100g"
        float protein "grams"
        float carbs "grams"
        float fats "grams"
        boolean is_custom
        int created_by FK
        datetime created_at
    }
    
    MEAL_PLAN {
        int id PK
        int user_id FK
        date date "unique per user per day"
        int goal_calories "default 2000"
        text notes
        datetime created_at
    }
    
    MEAL_ENTRY {
        int id PK
        int meal_plan_id FK
        int food_id FK
        string meal_type "breakfast|lunch|dinner|snack"
        float quantity
        string unit "g|ml|cup|tbsp|piece|serving"
        datetime added_at
    }
    

 ```

### 🔗 Key Database Relationships
User ↔ MealPlan: One-to-Many (one user, many daily plans)

MealPlan ↔ Food: Many-to-Many through MealEntry (enables food reuse with different quantities)

Food ↔ FoodCategory: Many-to-One (organized nutrition database)

User ↔ Food: One-to-Many for custom foods (users can add personal foods)    
Recipes ↔ foods: are Many-to-Many through RECIPE_INGREDIENT table. This enables a recipe to have many foods (ingredients), and each food can be part of many recipes, with extra data like quantity/unit per ingredient.

### full detaield 

<img width="2107" height="2344" alt="Untitled diagram-2025-10-15-231804" src="https://github.com/user-attachments/assets/eaba3b91-b0e1-465a-b386-b7e114141eb1" />


## 🎯 Development Roadmap

| Phase          | Focus & Key Deliverables                       |
|----------------|------------------------------------------------|
| Foundation     | Project structure, models, admin interface     |
| Authentication | User auth system, basic templates, CSS         |
| Core Features  | Dashboard, food management, meal tracking      |
| Advanced       | Recipe system, mobile optimization             |
| Production     | Documentation, testing, deployment             |

## 📊 Sample Data Loaded

- 18 food categories (Proteins, Vegetables, Fruits, Grains & Starches, Dairy, Healthy Fats, Beverages, Snacks, ....)
- 100+ demo foods seeded for testing purposes
- Easy to expand with more foods via the loader script

### Example foods:
| Name                         | Category     | Calories | Protein |
|------------------------------|-------------|----------|---------|
| Apple (with skin)            | Fruits      | 52       | 0.3     |
| Banana                       | Fruits      | 89       | 1.1     |
| Chicken Breast (skinless)    | Proteins    | 165      | 31.0    |
| Greek Yogurt (plain)         | Proteins    | 59       | 10.0    |
| Eggs (whole)                 | Proteins    | 155      | 13.0    |
| Broccoli                     | Vegetables  | 34       | 2.8     |
| Carrots                      | Vegetables  | 41       | 0.9     |

_(...and more—see admin for full list)_


## Installation Guide

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip
- virtualenv (recommended)

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/Tariq-Alhusban/Capstone-Project.git
cd nutritrack
```

2. **Create and activate virtual environment:**
```bash
python -m pip install pipenv
python -m pipenv install
python -m pipenv shell   
```

3. **Install dependencies:**
```bash
pip install django psycopg2-binary
```

4. **Configure PostgreSQL database:**
   - Create a PostgreSQL database named `nutritrack`
   - Update database settings in `nutritrack/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nutritrack',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser:**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional):**
```bash
python manage.py shell
# In Python shell:
from nutrition.models import FoodCategory, Food
FoodCategory.objects.create(name="Fruits", icon="🍎")
FoodCategory.objects.create(name="Vegetables", icon="🥬")
Food.objects.create(name="Apple", category_id=1, calories=52, protein=0.3, carbs=14, fats=0.2)
```

8. **Run the development server:**
```bash
python manage.py runserver
```

9. **Access the application:**
   - Open browser to `http://127.0.0.1:8000`
   - Register a new account or use superuser credentials

## User Stories

### Authentication & User Management
- As a user, I can register for an account to start tracking my nutrition
- As a user, I can log in securely to access my personal data
- As a user, I can log out to protect my privacy

### Daily Meal Tracking
- As a user, I can view my daily nutrition dashboard with calorie and macro summaries
- As a user, I can add foods to breakfast, lunch, dinner, or snack categories
- As a user, I can specify portions using various units (grams, cups, pieces)
- As a user, I can edit or delete meal entries to correct mistakes
- As a user, I can set daily calorie goals and track my progress

### Food Management
- As a user, I can search the food database to find nutritional information
- As a user, I can add custom foods with their nutritional data
- As a user, I can view detailed information about any food item
- As a user, I can quickly add frequently used foods to my meals

### Recipe Management
- As a user, I can create custom recipes with multiple ingredients
- As a user, I can view my saved recipes with calculated nutritional totals
- As a user, I can add entire recipes to my meal plan
- As a user, I can specify ingredient quantities and cooking notes

### Analytics & Insights
- As a user, I can view daily and weekly summaries of my nutrition intake
- As a user, I can see trends in my eating patterns over time
- As a user, I can copy previous day's meals for consistent planning
- As a user, I can track my progress toward nutritional goals

### Mobile Experience
- As a mobile user, I can access all features with touch-friendly interfaces
- As a mobile user, I can use the responsive navigation menu
- As a mobile user, I can input data with optimized form controls

## Challenges Encountered & Solutions

### 1. Complex Data Relationships
**Challenge:** Managing relationships between Users, MealPlans, Foods, and Recipes with proper foreign keys and many-to-many relationships.

**Solution:** Implemented a clear model hierarchy with Django's ORM, using `get_or_create()` for meal plans and proper foreign key constraints with CASCADE/SET_NULL deletion policies.

### 2. Unit Conversion System
**Challenge:** Supporting multiple units (grams, cups, tablespoons) with accurate nutritional calculations.

**Solution:** Created a `get_scale_factor()` method in both MealEntry and RecipeIngredient models to convert all units to a 100g baseline for consistent calculations.

### 3. Mobile Responsiveness
**Challenge:** Creating a mobile-first design that works across all device sizes.

**Solution:** Implemented CSS Grid and Flexbox with mobile-first media queries, custom CSS variables for consistent theming(with the help of AI language models), and JavaScript(with the help of AI language models) for mobile-specific interactions like touch navigation.

### 4. Real-time Recipe Calculations
**Challenge:** Dynamically calculating recipe nutritional totals as users add ingredients.

**Solution:** Implemented JavaScript event listeners with real-time calculation functions that update nutritional summaries instantly when ingredients are modified.

### 5. Data Integrity & User Experience
**Challenge:** Preventing duplicate meal plans and ensuring data consistency while maintaining good UX.

**Solution:** Used Django's `unique_together` constraints, form validation, and user-friendly error messages with Django's messages framework.

## Future Enhancements

### High Priority
- **User Profiles**: Customizable goals, dietary preferences, and personal metrics
- **Data Export**: CSV/PDF export for meal history and nutritional reports
- **Advanced Search**: Filter foods by nutritional criteria and dietary restrictions
- **Meal Planning**: Weekly meal prep and planning features

### Medium Priority
- **Social Features**: Share recipes and meal plans with other users
- **Photo Upload**: Add food photos to custom entries and recipes
- **Barcode Scanning**: Mobile barcode scanning for quick food entry
- **Nutrition Targets**: Micronutrient tracking (vitamins, minerals)

### Low Priority
- **API Integration**: Connect with fitness trackers and external food databases
- **Machine Learning**: Personalized meal recommendations based on history
- **Advanced Analytics**: Detailed nutrition trend analysis and reporting

## Security Considerations
>(with the help of AI language models)

- CSRF protection enabled for all forms
- User authentication required for all data access
- SQL injection prevention through Django ORM
- XSS protection via Django template auto-escaping
- Secure session management with Django's built-in system

## Performance Optimizations

- Database query optimization with `select_related()` and `prefetch_related()`
- Efficient pagination for large datasets
- CSS and JavaScript minification ready for production
- Database indexes on frequently queried fields
- Optimized mobile CSS with minimal JavaScript

## Testing Strategy

The application includes comprehensive manual testing coverage:
- User authentication flows
- CRUD operations for all models
- Form validation and error handling
- Mobile responsiveness across devices
- Database integrity and relationships

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with clear description

## License

This project is developed as an educational capstone project.

---

**Developed by:** [Tariq Alhusban]  
**Course:** Django Web Development Capstone  
**Date:** October 2025  
**Version:** 1.0.0
  
