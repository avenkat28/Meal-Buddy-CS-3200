from flask import Blueprint, request, jsonify
from backend.db_connection import db

meal_plans = Blueprint('meal_plans', __name__)


# Route 1: GET /meal_plans/<id>/planned_meals
@meal_plans.route('/meal_plans/<int:plan_id>/planned_meals', methods=['GET'])
def get_planned_meals(plan_id):
    """Get all planned meals for a specific meal plan"""
    cursor = db.get_db().cursor()
    query = '''
        SELECT pm.planned_meal_id, pm.day_of_week, pm.meal_type, 
               m.meal_id, m.meal_name, m.calories
        FROM planned_meals pm
        JOIN meals m ON pm.meal_id = m.meal_id
        WHERE pm.plan_id = %s
        ORDER BY FIELD(pm.day_of_week,'Mon','Tue','Wed','Thu','Fri','Sat','Sun'),
                 FIELD(pm.meal_type,'breakfast','lunch','dinner')
    '''
    cursor.execute(query, (plan_id,))
    results = cursor.fetchall()

    return jsonify(results), 200


# Route 2: POST /meal_plans/<id>/planned_meals
@meal_plans.route('/meal_plans/<int:plan_id>/planned_meals', methods=['POST'])
def add_planned_meal(plan_id):
    """Add a new meal to the meal plan"""
    data = request.json
    cursor = db.get_db().cursor()

    query = '''
        INSERT INTO planned_meals (plan_id, meal_id, day_of_week, meal_type)
        VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(query, (
        plan_id,
        data['meal_id'],
        data['day_of_week'],
        data['meal_type']
    ))
    db.get_db().commit()

    return jsonify({'message': 'Meal added successfully', 'plan_id': plan_id}), 201


# Route 3: GET /meal_plans/<id>/ingredients
@meal_plans.route('/meal_plans/<int:plan_id>/ingredients', methods=['GET'])
def get_grocery_list(plan_id):
    """Get complete grocery list for meal plan"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT i.ingredient_id, i.ingredient_name, i.category,
               SUM(mi.quantity) as total_quantity, mi.unit
        FROM planned_meals pm
        JOIN meal_ingredients mi ON pm.meal_id = mi.meal_id
        JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
        WHERE pm.plan_id = %s
        GROUP BY i.ingredient_id, i.ingredient_name, i.category, mi.unit
        ORDER BY i.category, i.ingredient_name
    '''
    cursor.execute(query, (plan_id,))
    results = cursor.fetchall()

    return jsonify(results), 200


# Route 4: GET /meal_plans/<id>/shared_ingredients
@meal_plans.route('/meal_plans/<int:plan_id>/shared_ingredients', methods=['GET'])
def get_shared_ingredients(plan_id):
    """Get ingredients used in multiple meals"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT i.ingredient_name, COUNT(DISTINCT pm.meal_id) as usage_count,
               GROUP_CONCAT(DISTINCT m.meal_name) as used_in_meals
        FROM planned_meals pm
        JOIN meal_ingredients mi ON pm.meal_id = mi.meal_id
        JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
        JOIN meals m ON pm.meal_id = m.meal_id
        WHERE pm.plan_id = %s
        GROUP BY i.ingredient_id, i.ingredient_name
        HAVING COUNT(DISTINCT pm.meal_id) > 1
        ORDER BY usage_count DESC
    '''
    cursor.execute(query, (plan_id,))
    results = cursor.fetchall()

    return jsonify(results), 200


# Route 5: GET /meal_plans/<id>/weekly_nutrition
@meal_plans.route('/meal_plans/<int:plan_id>/weekly_nutrition', methods=['GET'])
def get_weekly_nutrition(plan_id):
    """Get nutritional summary for entire week"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT 
            SUM(m.calories) as total_calories,
            SUM(m.protein_g) as total_protein,
            SUM(m.carbs_g) as total_carbs,
            SUM(m.fat_g) as total_fat,
            COUNT(DISTINCT pm.day_of_week) as days_planned
        FROM planned_meals pm
        JOIN meals m ON pm.meal_id = m.meal_id
        WHERE pm.plan_id = %s
    '''
    cursor.execute(query, (plan_id,))
    result = cursor.fetchone()

    return jsonify(result), 200