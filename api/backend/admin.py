from flask import Blueprint, request, jsonify, Response
from backend.db_connection import db
import csv
from io import StringIO

admin = Blueprint('admin', __name__)


# Route 1: GET /admin/error_logs
@admin.route('/admin/error_logs', methods=['GET'])
def get_error_logs():
    """Get system error logs with optional filters"""
    # Get query parameters
    resolved = request.args.get('resolved', 'false').lower()
    severity = request.args.get('severity')
    export_csv = request.args.get('export', 'false').lower() == 'true'
    
    cursor = db.get_db().cursor()
    
    # Base query
    query = '''
        SELECT error_id, error_type, error_message, 
               severity, timestamp, is_resolved
        FROM error_logs
        WHERE 1=1
    '''
    params = []
    
    # Add filters
    if resolved == 'false':
        query += ' AND is_resolved = FALSE'
    elif resolved == 'true':
        query += ' AND is_resolved = TRUE'
    
    if severity:
        query += ' AND severity = %s'
        params.append(severity)
    
    query += ' ORDER BY timestamp DESC'
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    # Export as CSV if requested
    if export_csv:
        si = StringIO()
        writer = csv.writer(si)
        
        # Write header
        writer.writerow(['error_id', 'error_type', 'error_message', 
                        'severity', 'timestamp', 'is_resolved'])
        
        # Write data
        for row in results:
            writer.writerow([
                row['error_id'],
                row['error_type'],
                row['error_message'],
                row['severity'],
                row['timestamp'],
                row['is_resolved']
            ])
        
        output = si.getvalue()
        return Response(
            output,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=error_logs.csv'}
        )
    
    return jsonify(results), 200


# Route 2: PUT /admin/error_logs
@admin.route('/admin/error_logs/<int:error_id>', methods=['PUT'])
def update_error_log(error_id):
    """Mark an error as resolved"""
    data = request.json
    cursor = db.get_db().cursor()
    
    query = '''
        UPDATE error_logs
        SET is_resolved = %s
        WHERE error_id = %s
    '''
    
    cursor.execute(query, (data.get('is_resolved', True), error_id))
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Error log not found'}), 404
    
    return jsonify({'message': 'Error log updated successfully'}), 200


# Route 3: GET /admin/meal_plans
@admin.route('/admin/meal_plans', methods=['GET'])
def get_all_meal_plans():
    """Get all meal plans with status filtering"""
    status_filter = request.args.get('status')
    
    cursor = db.get_db().cursor()
    
    query = '''
        SELECT mp.plan_id, u.username, mp.status,
               mp.week_start, mp.week_end, mp.created_at
        FROM meal_plans mp
        JOIN users u ON mp.user_id = u.user_id
        WHERE 1=1
    '''
    params = []
    
    if status_filter:
        query += ' AND mp.status = %s'
        params.append(status_filter)
    
    # Order by problematic statuses first
    query += '''
        ORDER BY FIELD(mp.status, 'failed', 'corrupted', 'draft', 'complete'),
                 mp.created_at DESC
    '''
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    return jsonify(results), 200


# Route 4: GET /admin/ingredients/unmatched
@admin.route('/admin/ingredients/unmatched', methods=['GET'])
def get_unmatched_ingredients():
    """Get ingredients missing standardized names for grocery matching"""
    cursor = db.get_db().cursor()
    
    query = '''
        SELECT ingredient_id, ingredient_name, category
        FROM ingredients
        WHERE standardized_name IS NULL
           OR standardized_name = ''
        ORDER BY category, ingredient_name
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    return jsonify({
        'count': len(results),
        'unmatched_ingredients': results
    }), 200


# Route 5: GET /admin/ingredients/duplicates
@admin.route('/admin/ingredients/duplicates', methods=['GET'])
def get_duplicate_ingredients():
    """Get duplicate ingredient entries that need cleaning"""
    cursor = db.get_db().cursor()
    
    query = '''
        SELECT ingredient_name, 
               COUNT(*) AS duplicate_count,
               GROUP_CONCAT(ingredient_id) AS ingredient_ids
        FROM ingredients
        GROUP BY ingredient_name
        HAVING COUNT(*) > 1
        ORDER BY duplicate_count DESC
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    return jsonify({
        'count': len(results),
        'duplicates': results
    }), 200


# Route 6: DELETE /admin/ingredients/duplicates
@admin.route('/admin/ingredients/duplicates/<int:ingredient_id>', methods=['DELETE'])
def delete_duplicate_ingredient(ingredient_id):
    """Delete a duplicate ingredient entry"""
    cursor = db.get_db().cursor()
    
    # First check if this ingredient is being used
    check_query = '''
        SELECT COUNT(*) as usage_count
        FROM meal_ingredients
        WHERE ingredient_id = %s
    '''
    cursor.execute(check_query, (ingredient_id,))
    usage = cursor.fetchone()
    
    if usage['usage_count'] > 0:
        return jsonify({
            'error': 'Cannot delete ingredient that is being used in meals',
            'usage_count': usage['usage_count']
        }), 400
    
    # Delete the ingredient
    delete_query = '''
        DELETE FROM ingredients
        WHERE ingredient_id = %s
    '''
    cursor.execute(delete_query, (ingredient_id,))
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    return jsonify({'message': 'Duplicate ingredient deleted successfully'}), 200


# Route 7: GET /admin/api_logs
@admin.route('/admin/api_logs', methods=['GET'])
def get_api_logs():
    """Get API performance metrics grouped by service"""
    time_range = request.args.get('time_range', '24h')  # 24h, 7d, 30d
    
    cursor = db.get_db().cursor()
    
    # Determine time filter
    time_filter = ''
    if time_range == '24h':
        time_filter = 'AND timestamp >= NOW() - INTERVAL 24 HOUR'
    elif time_range == '7d':
        time_filter = 'AND timestamp >= NOW() - INTERVAL 7 DAY'
    elif time_range == '30d':
        time_filter = 'AND timestamp >= NOW() - INTERVAL 30 DAY'
    
    query = f'''
        SELECT api_service,
               COUNT(*) AS request_count,
               AVG(response_time_ms) AS avg_response_time_ms,
               MIN(response_time_ms) AS min_response_time_ms,
               MAX(response_time_ms) AS max_response_time_ms,
               SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS error_count
        FROM api_logs
        WHERE 1=1 {time_filter}
        GROUP BY api_service
        ORDER BY avg_response_time_ms DESC
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    return jsonify({
        'time_range': time_range,
        'services': results
    }), 200


# Route 8: GET /admin/system_health (Bonus route)
@admin.route('/admin/system_health', methods=['GET'])
def get_system_health():
    """Get overall system health summary"""
    cursor = db.get_db().cursor()
    
    # Get error count
    cursor.execute('''
        SELECT COUNT(*) as unresolved_errors
        FROM error_logs
        WHERE is_resolved = FALSE
    ''')
    error_count = cursor.fetchone()['unresolved_errors']
    
    # Get unmatched ingredients count
    cursor.execute('''
        SELECT COUNT(*) as unmatched_count
        FROM ingredients
        WHERE standardized_name IS NULL OR standardized_name = ''
    ''')
    unmatched_count = cursor.fetchone()['unmatched_count']
    
    # Get failed meal plans count
    cursor.execute('''
        SELECT COUNT(*) as failed_plans
        FROM meal_plans
        WHERE status IN ('failed', 'corrupted')
    ''')
    failed_plans = cursor.fetchone()['failed_plans']
    
    # Determine overall status
    if error_count > 10 or failed_plans > 5:
        status = 'critical'
    elif error_count > 5 or unmatched_count > 20:
        status = 'warning'
    else:
        status = 'healthy'
    
    return jsonify({
        'status': status,
        'unresolved_errors': error_count,
        'unmatched_ingredients': unmatched_count,
        'failed_meal_plans': failed_plans,
        'timestamp': db.get_db().cursor().execute('SELECT NOW()').fetchone()[0]
    }), 200
