from flask import Blueprint, request, jsonify
from backend.db_connection import db

planned_meals = Blueprint('planned_meals', __name__)


# Route 1: GET /planned_meals/<id>
@planned_meals.route('/planned_meals/<int:planned_meal_id>', methods=['GET'])
def get_planned_meal(planned_meal_id):
    """Get details of a specific planned meal"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT pm.planned_meal_id, pm.plan_id, pm.day_of_week, pm.meal_type,
               m.meal_id, m.meal_name, m.calories, m.difficulty
        FROM planned_meals pm
        JOIN meals m ON pm.meal_id = m.meal_id
        WHERE pm.planned_meal_id = %s
    '''
    cursor.execute(query, (planned_meal_id,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'Planned meal not found'}), 404

    return jsonify(result), 200


# Route 2: PUT /planned_meals/<id>
@planned_meals.route('/planned_meals/<int:planned_meal_id>', methods=['PUT'])
def update_planned_meal(planned_meal_id):
    """Update/swap a planned meal"""
    data = request.json
    cursor = db.get_db().cursor()

    query = '''
        UPDATE planned_meals
        SET meal_id = %s
        WHERE planned_meal_id = %s
    '''
    cursor.execute(query, (data['meal_id'], planned_meal_id))
    db.get_db().commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Planned meal not found'}), 404

    return jsonify({'message': 'Planned meal updated successfully'}), 200


# Route 3: DELETE /planned_meals/<id>
@planned_meals.route('/planned_meals/<int:planned_meal_id>', methods=['DELETE'])
def delete_planned_meal(planned_meal_id):
    """Remove a meal from the plan"""
    cursor = db.get_db().cursor()

    query = '''
        DELETE FROM planned_meals
        WHERE planned_meal_id = %s
    '''
    cursor.execute(query, (planned_meal_id,))
    db.get_db().commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Planned meal not found'}), 404

    return jsonify({'message': 'Meal removed from plan'}), 200


# Route 4: GET /users/<id>/meal_reports
@planned_meals.route('/users/<int:user_id>/meal_reports', methods=['GET'])
def get_meal_reports(user_id):
    """Generate custom meal reports"""
    report_type = request.args.get('type', 'category')  # category, cost, etc.

    cursor = db.get_db().cursor()

    if report_type == 'category':
        query = '''
            SELECT i.category, COUNT(*) as usage_count
            FROM meal_plans mp
            JOIN planned_meals pm ON mp.plan_id = pm.plan_id
            JOIN meal_ingredients mi ON pm.meal_id = mi.meal_id
            JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
            WHERE mp.user_id = %s
            GROUP BY i.category
            ORDER BY usage_count DESC
        '''
    else:
        # Default query
        query = '''
            SELECT pm.day_of_week, m.meal_name, m.calories
            FROM meal_plans mp
            JOIN planned_meals pm ON mp.plan_id = pm.plan_id
            JOIN meals m ON pm.meal_id = m.meal_id
            WHERE mp.user_id = %s
            ORDER BY FIELD(pm.day_of_week,'Mon','Tue','Wed','Thu','Fri','Sat','Sun')
        '''

    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    return jsonify(results), 200


# Route 5: GET /ingredients
@planned_meals.route('/ingredients', methods=['GET'])
def get_all_ingredients():
    """Get list of all ingredients"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT ingredient_id, ingredient_name, category, 
               standardized_name
        FROM ingredients
        ORDER BY category, ingredient_name
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    return jsonify(results), 200