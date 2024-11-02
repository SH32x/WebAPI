# Web Application Deployment Guide

## Prerequisites
Before you start, make sure you have installed or set up the following:
- Python 3.9 (or newer)
- Git
- Google Cloud SDK
- A Google Cloud account with billing enabled

## Initial Setup

### 1. Clone the Repository
```bash
git clone https://github.com/SH32x/WebAPI
```

### 2. Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project, note your 'project id'

### 3. Initialize Google Cloud SDK
```bash
gcloud init
gcloud config set project 'project id'
```

### 4. Enable Required APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

## Database Setup

### 1. Create Cloud SQL Instance
1. Go to the [Cloud SQL Instances](https://console.cloud.google.com/sql) and click 'Create Instance'
2. Choose 'MySQL', set a password for the 'root' user.
3. Select DB version and plans (I chose Enterprise)

### 2. Create Database
In place of 'instance-name' add your own instance's name
```bash
gcloud sql databases create db-name --instance=instance-name
```

### 3. Create Database User
Again, replace placeholders with your own values.
```bash
gcloud sql users create db-user \
    --instance=instance-name \
    --password=db-password
```

## Secret Manager Setup

### 1. Create Required Secrets
The names of the secrets should correspond to 'secret_key', 'db-user', etc., if you
wish to use different names make sure to change the references in 'config.py' as well.

Make sure that "db-user-value", "db-password-value, and "db-name-value" correspond to the actual name
and credentials of your cloud database.
```bash
# Create secrets
gcloud secrets create secret_key --replication-policy="automatic"
gcloud secrets create db-user --replication-policy="automatic"
gcloud secrets create db-password --replication-policy="automatic"
gcloud secrets create db-name --replication-policy="automatic"

# Add secret values
echo -n "secret-key-value" | gcloud secrets versions add secret_key --data-file=-
echo -n "db-user-value" | gcloud secrets versions add db-user --data-file=-
echo -n "db-password-value" | gcloud secrets versions add db-password --data-file=-
echo -n "db-name-value" | gcloud secrets versions add db-name --data-file=-
```

### 2. Set IAM Permissions
```bash
gcloud projects add-iam-policy-binding 'project-id-value' \
    --member="serviceAccount:project-id-value@appspot.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## Application Configuration and Deployment

### 1. Update config.py
Replace the following values in `config.py`:
- `project_id="webapi-439022"` with your project ID
- In the SQLALCHEMY_DATABASE_URI, replace the socket name with your instance's socket name:
  ```python
  ?unix_socket=/cloudsql/<your-project-id>:<region>:instance-name
  ```


### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Deploy to App Engine
```bash
gcloud app deploy
```

### 4. View Application
```bash
gcloud app browse
```
