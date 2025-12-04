from flask import Blueprint, request, jsonify
from backend.db_connection import db

meals = Blueprint('meals', __name__)


# Route 1: GET /meals
@meals.route('/meals', methods=['GET'])
def get_all_meals():
    """Get all meals with optional filters"""
    # Get query parameters
    difficulty = request.args.get('difficulty')
    max_time = request.args.get('max_time', type=int)
    diet_type = request.args.get('diet_type')

    cursor = db.get_db().cursor()

    # Base query
    query = '''
        SELECT m.meal_id, m.meal_name, m.difficulty, 
               m.cooking_time_minutes, m.calories
        FROM meals m
        WHERE 1=1
    '''
    params = []

    # Add filters
    if difficulty:
        query += ' AND m.difficulty = %s'
        params.append(difficulty)

    if max_time:
        query += ' AND m.cooking_time_minutes <= %s'
        params.append(max_time)

    query += ' ORDER BY m.meal_name'

    cursor.execute(query, params)
    results = cursor.fetchall()

    return jsonify(results), 200


# Route 2: GET /meals/<id>
@meals.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal_details(meal_id):
    """Get complete details for a specific meal"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT meal_id, meal_name, difficulty, cooking_time_minutes,
               calories, protein_g, carbs_g, fat_g, recipe_steps
        FROM meals
        WHERE meal_id = %s
    '''
    cursor.execute(query, (meal_id,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'Meal not found'}), 404

    return jsonify(result), 200


# Route 3: GET /meals/<id>/ingredients
@meals.route('/meals/<int:meal_id>/ingredients', methods=['GET'])
def get_meal_ingredients(meal_id):
    """Get all ingredients for a specific meal"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT i.ingredient_id, i.ingredient_name, i.category,
               mi.quantity, mi.unit
        FROM meal_ingredients mi
        JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
        WHERE mi.meal_id = %s
        ORDER BY i.category, i.ingredient_name
    '''
    cursor.execute(query, (meal_id,))
    results = cursor.fetchall()

    return jsonify(results), 200


# Route 4: GET /meals/<id>/costs
@meals.route('/meals/<int:meal_id>/costs', methods=['GET'])
def get_meal_costs(meal_id):
    """Get cost breakdown for a meal"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT meal_id, total_cost, cost_per_serving, 
               calculation_date
        FROM meal_cost_history
        WHERE meal_id = %s
        ORDER BY calculation_date DESC
        LIMIT 1
    '''
    cursor.execute(query, (meal_id,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'message': 'No cost data available'}), 404

    return jsonify(result), 200


# Route 5: GET /meals/suggestions
@meals.route('/meals/suggestions', methods=['GET'])
def get_meal_suggestions():
    """Get meal suggestions based on user inventory"""
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({'error': 'user_id parameter required'}), 400

    cursor = db.get_db().cursor()

    query = '''
        SELECT DISTINCT m.meal_id, m.meal_name, m.difficulty,
               m.cooking_time_minutes, m.calories,
               COUNT(DISTINCT mi.ingredient_id) as matching_ingredients
        FROM meals m
        JOIN meal_ingredients mi ON m.meal_id = mi.meal_id
        JOIN inventory inv ON inv.ingredient_id = mi.ingredient_id
        WHERE inv.user_id = %s
        GROUP BY m.meal_id, m.meal_name, m.difficulty, 
                 m.cooking_time_minutes, m.calories
        ORDER BY matching_ingredients DESC
        LIMIT 10
    '''
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    return jsonify(results), 200