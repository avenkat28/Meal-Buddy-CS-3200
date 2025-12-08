DROP DATABASE IF EXISTS MealBuddy;
CREATE DATABASE MealBuddy;
USE MealBuddy;

-- User Profiles

CREATE TABLE users (
   user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   username VARCHAR(100) NOT NULL,
   email VARCHAR(255) UNIQUE NOT NULL,
   password_hash VARCHAR(255) NOT NULL,
   user_type ENUM('regular', 'admin') DEFAULT 'regular',
   account_status ENUM('active', 'suspended', 'deleted') DEFAULT 'active',
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   last_login TIMESTAMP NULL
);

CREATE TABLE dietary_preferences (
   preference_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL
);

CREATE TABLE user_dietary_preferences (
   user_id BIGINT,
   preference_id BIGINT,
   PRIMARY KEY (user_id, preference_id),
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
   FOREIGN KEY (preference_id) REFERENCES dietary_preferences(preference_id) ON DELETE CASCADE
);

CREATE TABLE user_goals (
   goal_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   user_id BIGINT NOT NULL,
   goal_description TEXT NOT NULL,
   target_date DATE,
   is_active BOOLEAN DEFAULT TRUE,
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Meals + Ingredients

CREATE TABLE meals (
meal_id BIGINT PRIMARY KEY AUTO_INCREMENT,
meal_name VARCHAR(255) NOT NULL,
difficulty ENUM('easy','medium','hard'),
cooking_time_minutes INT,
   calories INT,
   protein_g DECIMAL(10,2),
   carbs_g DECIMAL(10,2),
   fat_g DECIMAL(10,2),
   sodium_mg DECIMAL(10,2),
   recipe_steps TEXT
);

CREATE TABLE ingredients (
   ingredient_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   ingredient_name VARCHAR(255) NOT NULL,
   category VARCHAR(100),
   is_active BOOLEAN DEFAULT TRUE,
   standardized_name VARCHAR(255),
   last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE meal_ingredients (
   meal_id BIGINT,
   ingredient_id BIGINT,
   quantity DECIMAL(10,2) NOT NULL,
   unit VARCHAR(50) NOT NULL,
   PRIMARY KEY (meal_id, ingredient_id),
   FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE,
   FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
);

-- Meal Planning

CREATE TABLE meal_plans (
plan_id BIGINT PRIMARY KEY AUTO_INCREMENT,
user_id BIGINT NOT NULL,
week_start DATE NOT NULL,
week_end DATE NOT NULL,
status ENUM('draft','complete','corrupted','failed') DEFAULT 'draft',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE planned_meals (
   planned_meal_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   plan_id BIGINT NOT NULL,
   meal_id BIGINT NOT NULL,
   day_of_week ENUM('Mon','Tue','Wed','Thu','Fri','Sat','Sun'),
   meal_type ENUM('breakfast','lunch','dinner','snack'),
   FOREIGN KEY (plan_id) REFERENCES meal_plans(plan_id) ON DELETE CASCADE,
   FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE
);

-- Grocery List

CREATE TABLE grocery_list (
   gl_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   user_id BIGINT NOT NULL,
   date_generated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE grocery_list_ingredients (
   gl_id BIGINT NOT NULL,
   ingredient_id BIGINT NOT NULL,
   quantity DECIMAL(10,2),
   unit VARCHAR(50),
   PRIMARY KEY (gl_id, ingredient_id),
   FOREIGN KEY (gl_id) REFERENCES grocery_list(gl_id) ON DELETE CASCADE,
   FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
);

-- Inventory

CREATE TABLE inventory (
   inventory_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   user_id BIGINT NOT NULL,
   ingredient_id BIGINT NOT NULL,
   quantity DECIMAL(10,2),
   expiration_date DATE,
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
   FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
);

CREATE TABLE inventory_event_log (
   event_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   inventory_id BIGINT NOT NULL,
   user_id BIGINT NOT NULL,
   event_type ENUM('ADDED','USED','EXPIRED','DISCARDED','ADJUSTED'),
   event_quantity DECIMAL(10,2),
   event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id) ON DELETE CASCADE,
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Data

CREATE TABLE consumed_meals (
   consumed_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   user_id BIGINT NOT NULL,
   meal_id BIGINT NOT NULL,
   date_consumed DATE NOT NULL,
   serving_multiplier DECIMAL(5,2) DEFAULT 1.0,
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
   FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE
);

CREATE TABLE daily_nutrition_summary (
   summary_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   user_id BIGINT NOT NULL,
   summary_date DATE NOT NULL,
   calories INT,
   protein_g DECIMAL(10,2),
   carbs_g DECIMAL(10,2),
   fat_g DECIMAL(10,2),
   sodium_mg DECIMAL(10,2),
   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE meal_cost_history (
   cost_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   meal_id BIGINT NOT NULL,
   calculation_date DATE NOT NULL,
   total_cost DECIMAL(10,2),
   cost_per_serving DECIMAL(10,2),
   FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE
);

-- Admin

CREATE TABLE api_logs (
   log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   api_service VARCHAR(100),
   endpoint VARCHAR(255),
   request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   response_time_ms INT,
   status_code INT
);

CREATE TABLE error_logs (
   error_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   error_type VARCHAR(100),
   error_message TEXT,
   severity ENUM('info','warning','critical'),
   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   related_user_id BIGINT NULL,
   related_plan_id BIGINT NULL,
   related_ingredient_id BIGINT NULL,
   is_resolved BOOLEAN DEFAULT FALSE,
   resolved_by_admin_id BIGINT NULL,
   FOREIGN KEY (related_user_id) REFERENCES users(user_id),
   FOREIGN KEY (related_plan_id) REFERENCES meal_plans(plan_id),
   FOREIGN KEY (related_ingredient_id) REFERENCES ingredients(ingredient_id),
   FOREIGN KEY (resolved_by_admin_id) REFERENCES users(user_id)
);

CREATE TABLE data_validation_issues (
   validation_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   table_name VARCHAR(100),
   record_id BIGINT,
   issue_type VARCHAR(255),
   severity ENUM('minor','moderate','critical'),
   detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   is_fixed BOOLEAN DEFAULT FALSE,
   fixed_by_admin_id BIGINT NULL,
   FOREIGN KEY (fixed_by_admin_id) REFERENCES users(user_id)
);
