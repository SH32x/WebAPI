# config.py
# Handles secretmanager integration from gcloud
# Note: When deploying yourself, replace the following values:
# project_id="webapi-439022" with your own project's id
# access_secret('db-user') with the name of the defined secret in your project's Secret Manager
# access_secret('db-password') with the name of the defined secret in your project's Secret Manager
# access_secret('db-name') with the name of the defined secret in your project's Secret Manager
# access_secret('secret_key') with the name of the defined secret in your project's Secret Manager
# '?unix_socket=/cloudsql/webapi-439022:northamerica-northeast2:t345db' with whatever the socket link for your DB instance is

from google.cloud import secretmanager

def access_secret(secret_id, project_id="webapi-439022"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8").strip()
    except Exception as e:
        raise RuntimeError(f"Failed to access required secret: {secret_id}")

class Config:
    # Verifies authentication with the secret key
    SECRET_KEY = access_secret('secret_key')
    if not SECRET_KEY:
        raise RuntimeError("Authentication failed: Invalid secret key")
    
    # Access database credentials using correct secret names
    try:
        db_user = access_secret('db-user')      
        db_password = access_secret('db-password')  
        db_name = access_secret('db-name')    
    except Exception as e:
        raise RuntimeError("ERROR: Wrong credentials...")
    
    # Database URI for Cloud SQL
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{db_user}:{db_password}@/{db_name}'
        '?unix_socket=/cloudsql/webapi-439022:northamerica-northeast2:t345db'
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False