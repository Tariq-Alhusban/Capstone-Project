# 🍎 NutriTrack - Nutrition & Meal Planning App - Tariq Alhusban

![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.13.7-blue.svg)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)

> **NutriTrack** is a Django web application for daily nutrition tracking and meal planning. This capstone project demonstrates advanced Django development with M2M relationships, custom authentication, and mobile-responsive design.

 Users can create daily meal plans, log foods with macronutrient tracking, create reusable recipes, and view detailed nutritional summaries.

---


## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#-project-structure)
- [Data Model & Relationships & ERD](#-database-architecture-erd)
- [Development Roadmap](#-development-roadmap)
- [Sample Data Loaded and cheak ](#-sample-data-loaded)
- [new: Enhanced Admin Interface ](#enhanced-admin-interface)


## Features

### 🎯 Planned Features
- **User Authentication**: Secure registration, login, logout with personalized dashboards
- 🍽️ **Smart Meal Planning** - Track breakfast, lunch, dinner, and snacks with automatic nutrition calculations
- 🔍 **Advanced Food Database** - Searchable database with alot of foods and custom food creation
- 📝 **Recipe System** - Save and reuse multi-ingredient meal combinations
- 📊 **Progress Tracking** - Visual nutrition goals with real-time progress indicators
- **Responsive Design**: Mobile-friendly interface using CSS Grid and Flexbox


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


### Development Tools
- **Version Control**: Git & GitHub
- **Package Management**: pip & requirements.txt
- **Virtual Environment**: pipenv shell
- **Code Editor**: VS Code compatible


## 📁 Project Structure
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



## 🎯 Development Roadmap

| Phase          | Focus & Key Deliverables                       |
|----------------|------------------------------------------------|
| Foundation     | Project structure, models, admin interface     |
| Authentication | User auth system, basic templates, CSS         |
| Core Features  | Dashboard, food management, meal tracking      |
| Advanced       | Recipe system, mobile optimization             |
| Production     | Documentation, testing, deployment             |

## 📊 Sample Data Loaded

- 8 food categories (Proteins, Vegetables, Fruits, Grains & Starches, Dairy, Healthy Fats, Beverages, Snacks)
- 15+ demo foods seeded for testing purposes
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

### Live Demo - Backend Working!
Admin Interface (http://127.0.0.1:8000/admin/):

Browse 15 foods organized by categories

Create meal plans and add food entries

View nutrition calculations in real-time

Manage food categories with emoji icon

## Enhanced Admin Interface
Visual Progress Indicators for meal plan calorie goals

Advanced Filtering by category, date, user, custom foods

Inline Editing for meal entries within meal plans

Bulk Actions for efficient data management

Custom Display with nutrition summaries and progress bars

### 🧪 What You Can Test Right Now
Admin Login - Access comprehensive data management

Browse Foods - 15 items with complete nutrition profiles

Create Meal Plans - Test date constraints and user relationships

Add Meal Entries - Verify nutrition calculations and unit conversions

View Categories - Organized food browsing with emoji icons

Custom Foods - Admin can add new foods with full nutrition data