# Application runpoint file

# runpoint.py
import os
from dotenv import load_dotenv
from app import app

def verify_environment():
    """Verify critical environment variables before starting the application"""
    required_vars = [
        'FLASK_APP',
        'DATABASE_URL',
        'SECRET_KEY'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please check your .env file and make sure all required variables are set."
        )

if __name__ == '__main__':
    load_dotenv()  # Load environment variables from .env
    verify_environment()  # Verify environment before starting
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')


