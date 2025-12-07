from flask import Flask

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev'  # Change in production
    
    # Import database connection
    from backend.db_connection import db
    
    # Register close_db function to run after each request
    app.teardown_appcontext(db.close_db)
    
    # Import and register blueprints
    from backend.meal import meals
    from backend.meal_plan import meal_plans
    from backend.planned_meals import planned_meals
    from backend.user import users
    from backend.admin import admin
    
    # Register all blueprints with /api prefix
    app.register_blueprint(meals, url_prefix='/api')
    app.register_blueprint(meal_plans, url_prefix='/api')
    app.register_blueprint(planned_meals, url_prefix='/api')
    app.register_blueprint(users, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/api')
    
    # Simple health check route
    @app.route('/')
    def home():
        return {
            'status': 'running',
            'message': 'MealBuddy API',
            'version': '1.0'
        }
    
    @app.route('/api')
    def api_home():
        return {
            'status': 'running',
            'available_endpoints': [
                '/api/meals',
                '/api/meal_plans/<id>/planned_meals',
                '/api/planned_meals/<id>',
                '/api/users/<id>/inventory',
                '/api/admin/error_logs'
            ]
        }
    
    return app
