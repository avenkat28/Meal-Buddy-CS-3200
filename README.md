# MealBuddy - Meal Planning Made Easy 🍽️

**CS 3200 Database Design Project - Fall 2025**

## Team: Meal Planners

**Team Members:**
- Arya Venkat (venkat.ar@northeastern.edu) - Point Person
- Charles Rubin (rubin.ch@northeastern.edu)
- Aryan Madan (madan.ary@northeastern.edu)
- Pranav Bollineni (bollineni.p@northeastern.edu)
- Vyom Rai (rai.vy@northeastern.edu)

## Project Overview

MealBuddy is a comprehensive meal planning application designed for college students who want to eat healthy but struggle with time management, grocery shopping, and budget constraints. The app creates personalized weekly meal plans based on dietary preferences, budget, and schedule, complete with recipes and grocery lists from nearby stores.

### Key Features
- **Personalized Meal Planning**: AI-powered weekly meal plans tailored to user preferences
- **Smart Grocery Lists**: Automatic ingredient aggregation with cost tracking
- **Nutrition Tracking**: Comprehensive nutritional analytics and progress monitoring
- **Inventory Management**: Track ingredients and reduce food waste
- **Data Analytics**: Advanced reporting for fitness enthusiasts and data analysts
- **Admin Dashboard**: System monitoring and maintenance tools

## User Personas

1. **Jordan Thompson** (College Junior) - Primary user focused on healthy eating and meal prep
2. **Michael Johnson** (Data Analyst) - Fitness enthusiast requiring detailed nutritional data
3. **Sarah Martinez** (Young Adult) - Cooking enthusiast focused on minimizing food waste
4. **Emily Carter** (System Admin) - IT support maintaining backend systems

## Technology Stack

- **Backend**: Flask REST API with Python
- **Database**: MySQL 8.0
- **Frontend**: Streamlit
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker Desktop installed and running
- Git (for cloning the repository)
- 4GB+ RAM available for containers

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/avenkat28/Meal-Buddy-CS-3200.git
cd Meal-Buddy-CS-3200
```

### 2. Configure Environment Variables

The `.env` file is already included with default settings. If you need to change the database password:

```bash
# Edit .env file
MYSQL_ROOT_PASSWORD=your_secure_password_here
```

### 3. Start the Application

```bash
# Start all services (database, API, and Streamlit app)
docker compose up -d

# Check that all containers are running
docker compose ps
```

**First-time setup will take 2-3 minutes** as Docker:
1. Downloads the required images
2. Builds the API and Streamlit containers
3. Creates the MySQL database
4. Runs all SQL scripts to populate data

### 4. Access the Application

Once all containers are running:

- **Streamlit UI**: http://localhost:8501
- **Flask API**: http://localhost:8000
- **API Health Check**: http://localhost:8000/api

### 5. Stop the Application

```bash
# Stop all containers
docker compose down

# Stop and remove all data (including database)
docker compose down -v
```

## Project Structure

```
Meal-Buddy-CS-3200/
├── api/                          # Flask REST API
│   ├── backend/
│   │   ├── __init__.py          # App initialization & blueprint registration
│   │   ├── db_connection.py     # Database connection handler
│   │   ├── meal.py              # Meal routes (5 routes)
│   │   ├── meal_plan.py         # Meal plan routes (5 routes)
│   │   ├── planned_meals.py     # Planned meal routes (5 routes)
│   │   ├── user.py              # User routes (6 routes)
│   │   └── admin.py             # Admin routes (8 routes)
│   ├── app.py                   # Flask application entry point
│   ├── Dockerfile
│   └── requirements.txt
├── app/                          # Streamlit frontend
│   ├── src/
│   │   ├── Home.py              # Landing page
│   │   ├── modules/             # Reusable components
│   │   └── pages/               # Feature pages (10+ pages)
│   ├── Dockerfile
│   └── requirements.txt
├── database-files/              # SQL scripts (auto-executed on startup)
│   ├── schema.sql              # Database schema
│   ├── users.sql               # User mock data
│   ├── meals.sql               # Meal mock data
│   └── ...                     # Additional data files
├── docker-compose.yml          # Docker orchestration
├── .env                        # Environment variables
├── .env.example               # Environment template
└── README.md                  # This file
```

## API Documentation

### Blueprints & Routes

The API is organized into 5 blueprints with 29 total routes:

#### Meals Blueprint (`/api/meals`)
- `GET /meals` - List all meals with filters
- `GET /meals/{id}` - Get meal details
- `GET /meals/{id}/ingredients` - Get meal ingredients
- `GET /meals/{id}/costs` - Get cost breakdown
- `GET /meals/suggestions` - Get personalized suggestions

#### Meal Plans Blueprint (`/api/meal_plans`)
- `GET /meal_plans/{id}/planned_meals` - Get all planned meals
- `POST /meal_plans/{id}/planned_meals` - Add meal to plan
- `GET /meal_plans/{id}/ingredients` - Get grocery list
- `GET /meal_plans/{id}/shared_ingredients` - Get shared ingredients
- `GET /meal_plans/{id}/weekly_nutrition` - Get nutrition summary

#### Planned Meals Blueprint (`/api/planned_meals`)
- `GET /planned_meals/{id}` - Get planned meal details
- `PUT /planned_meals/{id}` - Update/swap meal
- `DELETE /planned_meals/{id}` - Remove meal from plan
- `GET /users/{id}/meal_reports` - Generate custom reports
- `GET /ingredients` - List all ingredients

#### Users Blueprint (`/api/users`)
- `GET /users/{id}/inventory` - Get user inventory
- `POST /users/{id}/inventory` - Add to inventory
- `GET /users/{id}/inventory/{ingredient_id}` - Get specific item
- `PUT /users/{id}/inventory/{ingredient_id}` - Update quantity
- `DELETE /users/{id}/inventory/{ingredient_id}` - Remove item
- `GET /users/{id}/nutrition_summary` - Get nutrition progress

#### Admin Blueprint (`/api/admin`)
- `GET /admin/error_logs` - View error logs
- `PUT /admin/error_logs/{id}` - Mark error as resolved
- `GET /admin/meal_plans` - View all meal plans
- `GET /admin/ingredients/unmatched` - Find unmatched ingredients
- `GET /admin/ingredients/duplicates` - Find duplicates
- `DELETE /admin/ingredients/duplicates/{id}` - Delete duplicate
- `GET /admin/api_logs` - View API performance metrics
- `GET /admin/system_health` - System health check

## Database Schema

The database includes 20+ tables covering:
- User management and authentication
- Meal catalog with ingredients and nutrition
- Meal planning and scheduling
- Inventory tracking
- Grocery list generation
- Analytics and reporting
- System administration and logging

## Development

### Viewing Logs

```bash
# View all logs
docker compose logs

# View specific service logs
docker compose logs api
docker compose logs app
docker compose logs db

# Follow logs in real-time
docker compose logs -f api
```

### Rebuilding After Code Changes

```bash
# Rebuild and restart specific service
docker compose up -d --build api

# Rebuild all services
docker compose up -d --build
```

### Accessing the Database

```bash
# Connect to MySQL container
docker exec -it mealbuddy-db mysql -u root -p

# Enter password from .env file (default: mealbuddy_secure_password_2024)
```

## Troubleshooting

### Containers won't start
```bash
# Check Docker Desktop is running
# Remove old containers and volumes
docker compose down -v
docker compose up -d
```

### Database connection errors
```bash
# Wait for database to fully initialize (can take 30-60 seconds)
docker compose logs db

# Ensure .env file has correct password
```

### Port already in use
```bash
# Change ports in docker-compose.yml if 3306, 8000, or 8501 are occupied
ports:
  - "3307:3306"  # Change first number only
```

## Demo Video

[Link to demo video will be added here]

## GitHub Repository

https://github.com/avenkat28/Meal-Buddy-CS-3200.git

## License

This project was created for educational purposes as part of CS 3200 at Northeastern University.

---

**Last Updated**: December 2025
