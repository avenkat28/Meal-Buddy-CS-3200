from backend import create_app
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
