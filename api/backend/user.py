from flask import Blueprint, request, jsonify
from backend.db_connection import db

users = Blueprint('users', __name__)


# Route 1: GET /users/<id>/inventory
@users.route('/users/<int:user_id>/inventory', methods=['GET'])
def get_user_inventory(user_id):
    """Get all inventory items for a user"""
    sort_by = request.args.get('sort_by', 'name')  # name or expiration

    cursor = db.get_db().cursor()

    query = '''
        SELECT inv.inventory_id, i.ingredient_id, i.ingredient_name,
               i.category, inv.quantity, inv.expiration_date
        FROM inventory inv
        JOIN ingredients i ON inv.ingredient_id = i.ingredient_id
        WHERE inv.user_id = %s
    '''

    if sort_by == 'expiration':
        query += ' ORDER BY inv.expiration_date ASC'
    else:
        query += ' ORDER BY i.ingredient_name'

    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    return jsonify(results), 200


# Route 2: POST /users/<id>/inventory
@users.route('/users/<int:user_id>/inventory', methods=['POST'])
def add_to_inventory(user_id):
    """Add new ingredient to user's inventory"""
    data = request.json
    cursor = db.get_db().cursor()

    query = '''
        INSERT INTO inventory (user_id, ingredient_id, quantity, expiration_date)
        VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(query, (
        user_id,
        data['ingredient_id'],
        data['quantity'],
        data.get('expiration_date')
    ))
    db.get_db().commit()

    return jsonify({
        'message': 'Ingredient added to inventory',
        'inventory_id': cursor.lastrowid
    }), 201


# Route 3: GET /users/<id>/inventory/<ingredient_id>
@users.route('/users/<int:user_id>/inventory/<int:ingredient_id>', methods=['GET'])
def get_inventory_item(user_id, ingredient_id):
    """Get specific inventory item"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT inv.inventory_id, i.ingredient_id, i.ingredient_name,
               inv.quantity, inv.expiration_date
        FROM inventory inv
        JOIN ingredients i ON inv.ingredient_id = i.ingredient_id
        WHERE inv.user_id = %s AND inv.ingredient_id = %s
    '''
    cursor.execute(query, (user_id, ingredient_id))
    result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'Inventory item not found'}), 404

    return jsonify(result), 200


# Route 4: PUT /users/<id>/inventory/<ingredient_id>
@users.route('/users/<int:user_id>/inventory/<int:ingredient_id>', methods=['PUT'])
def update_inventory(user_id, ingredient_id):
    """Update inventory quantity"""
    data = request.json
    cursor = db.get_db().cursor()

    query = '''
        UPDATE inventory
        SET quantity = %s
        WHERE user_id = %s AND ingredient_id = %s
    '''
    cursor.execute(query, (data['quantity'], user_id, ingredient_id))
    db.get_db().commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Inventory item not found'}), 404

    return jsonify({'message': 'Inventory updated successfully'}), 200


# Route 5: DELETE /users/<id>/inventory/<ingredient_id>
@users.route('/users/<int:user_id>/inventory/<int:ingredient_id>', methods=['DELETE'])
def remove_from_inventory(user_id, ingredient_id):
    """Remove ingredient from inventory"""
    cursor = db.get_db().cursor()

    query = '''
        DELETE FROM inventory
        WHERE user_id = %s AND ingredient_id = %s
    '''
    cursor.execute(query, (user_id, ingredient_id))
    db.get_db().commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Inventory item not found'}), 404

    return jsonify({'message': 'Item removed from inventory'}), 200


# Route 6: GET /users/<id>/nutrition_summary
@users.route('/users/<int:user_id>/nutrition_summary', methods=['GET'])
def get_nutrition_summary(user_id):
    """Get user's nutrition progress"""
    cursor = db.get_db().cursor()

    query = '''
        SELECT *
        FROM daily_nutrition_summary
        WHERE user_id = %s
        ORDER BY summary_date DESC
        LIMIT 7
    '''
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    return jsonify(results), 200