# config.py

import os
from dotenv import load_dotenv
from google.cloud import secretmanager

def access_secret(secret_id, project_id="webapi-439022"):
    """Access secret from Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception:
        return None

class Config:
    """Configuration class for Flask application settings"""
    # Use environment variables in development, secrets in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if is_production:
        db_user = access_secret('db_user')
        db_password = access_secret('db_password')
        db_name = access_secret('db_name')
        
        SQLALCHEMY_DATABASE_URI = (
            f'mysql+pymysql://{db_user}:{db_password}@/{db_name}'
            '?unix_socket=/cloudsql/webapi-439022:northamerica-northeast2:t345db'
        )
    else:
        load_dotenv()
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    SQLALCHEMY_TRACK_MODIFICATIONS = False