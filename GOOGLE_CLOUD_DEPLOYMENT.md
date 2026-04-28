# CyberShield-AI: Google Cloud Deployment Guide

## Overview
This guide explains how to deploy CyberShield-AI on Google Cloud Platform using Cloud Run, Firestore, and the Gemini AI API.

## Architecture
- **Frontend**: Deployed on Cloud Storage + Cloud CDN (or Cloud Run)
- **Backend**: Flask API on Cloud Run
- **Database**: Cloud Firestore or Cloud SQL (PostgreSQL)
- **AI Service**: Google Gemini API (via google-generativeai library)
- **Authentication**: Firebase Authentication
- **Storage**: Cloud Storage for logs and reports

## Prerequisites
1. Google Cloud Project created
2. `gcloud` CLI installed
3. Docker installed (for building container images)
4. Billing enabled on GCP project
5. Google AI API key from https://makersuite.google.com/app/apikey

## Step 1: Set Up Google Cloud Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  firestore.googleapis.com \
  storage-api.googleapis.com \
  cloudkms.googleapis.com \
  containerregistry.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```

## Step 2: Set Up Authentication & Environment

```bash
# Create a Secret Manager secret for the Google API Key
echo -n "your-google-api-key" | gcloud secrets create google-api-key --data-file=-

# Grant Cloud Run service access to the secret
gcloud secrets add-iam-policy-binding google-api-key \
  --member=serviceAccount:$PROJECT_ID@appspot.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

## Step 3: Create Firestore Database (Alternative to PostgreSQL)

```bash
# Create Firestore in native mode
gcloud firestore databases create --region=us-central1 --database-id=default

# Or use Cloud SQL for PostgreSQL
gcloud sql instances create cybershield-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1
```

## Step 4: Containerize the Backend

Create a `Dockerfile` in the backend directory:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "app:app"]
```

Update `requirements.txt` to include gunicorn:

```
gunicorn==22.0.0
```

## Step 5: Build and Push Container to Artifact Registry

```bash
# Create Artifact Registry repository
gcloud artifacts repositories create cybershield-ai \
  --repository-format=docker \
  --location=us-central1

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build the container
cd backend
docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/cybershield-ai/backend:latest .

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/$PROJECT_ID/cybershield-ai/backend:latest
```

## Step 6: Deploy Backend to Cloud Run

```bash
gcloud run deploy cybershield-backend \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/cybershield-ai/backend:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600 \
  --max-instances 100 \
  --set-env-vars "FLASK_ENV=production,DATABASE_URL=$DB_URL" \
  --set-secrets "GOOGLE_API_KEY=google-api-key:latest" \
  --allow-unauthenticated \
  --update-env-vars N8N_WEBHOOK_URL="https://your-n8n-instance.com/webhook-test/shieldai-alert"
```

## Step 7: Deploy Frontend to Cloud Storage + CDN

```bash
# Create Cloud Storage bucket
gsutil mb gs://$PROJECT_ID-cybershield-frontend

# Build the frontend
cd frontend
npm run build

# Upload to Cloud Storage
gsutil -m cp -r dist/* gs://$PROJECT_ID-cybershield-frontend/

# Make files public
gsutil acl ch -u AllUsers:R gs://$PROJECT_ID-cybershield-frontend

# Configure as static website
gsutil web set -m index.html -e 404.html gs://$PROJECT_ID-cybershield-frontend

# Create Cloud CDN load balancer (optional but recommended)
# This requires additional setup via Google Cloud Console
```

## Step 8: Set Up Cloud Monitoring & Logging

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=cybershield-backend" \
  --limit 50 \
  --format=json

# Create metric alerts
gcloud alpha monitoring policies create \
  --notification-channels=your-channel-id \
  --display-name="CyberShield Backend Error Rate"
```

## Step 9: Configure CORS (Update backend app.py)

Add support for your frontend URL:

```python
CORS(app, resources={r"/*": {
    "origins": ["https://your-frontend-domain.com"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})
```

## Step 10: Set Up CI/CD Pipeline (Cloud Build)

Create `cloudbuild.yaml`:

```yaml
steps:
  # Build Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-central1-docker.pkg.dev/$PROJECT_ID/cybershield-ai/backend:$COMMIT_SHA', '.']
    dir: 'backend'

  # Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-central1-docker.pkg.dev/$PROJECT_ID/cybershield-ai/backend:$COMMIT_SHA']

  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --filename=.
      - --image=us-central1-docker.pkg.dev/$PROJECT_ID/cybershield-ai/backend:$COMMIT_SHA
      - --location=us-central1
      - --output=/workspace/output

images:
  - 'us-central1-docker.pkg.dev/$PROJECT_ID/cybershield-ai/backend:$COMMIT_SHA'
```

## Step 11: Environment Configuration for Production

Update your `.env` file with production values:

```bash
# Set in Cloud Run environment variables
GOOGLE_API_KEY=<your-key> # From Secret Manager
DATABASE_URL=<postgres-connection-string>
FLASK_ENV=production
N8N_WEBHOOK_URL=<your-n8n-webhook>
```

## Step 12: Cost Optimization

1. **Cloud Run**: Enable min instances = 0 to save on idle time
2. **Cloud SQL**: Use small instances and set automatic backups
3. **Cloud Storage**: Set lifecycle policies to delete old logs
4. **Monitoring**: Use Google Cloud's cost monitoring tools

## Monitoring & Debugging

### View Cloud Run Logs
```bash
gcloud run logs read cybershield-backend --region us-central1 --limit 100
```

### Check AI Service Status
```bash
curl https://your-cloud-run-url/health
```

### Test AI Endpoints
```bash
curl -X POST https://your-cloud-run-url/ai/assess-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Security Best Practices

1. **API Keys**: Store in Cloud Secret Manager, never in code
2. **CORS**: Restrict to your frontend domain
3. **Authentication**: Implement Firebase Auth for user sessions
4. **Database**: Use VPC connectors for Cloud SQL access
5. **DDoS Protection**: Enable Cloud Armor on Cloud Load Balancer
6. **Secrets Rotation**: Rotate API keys regularly

## Troubleshooting

### Cloud Run Error: "Secret not found"
```bash
# Verify secret exists
gcloud secrets list

# Verify permissions
gcloud secrets get-iam-policy google-api-key
```

### Database Connection Issues
```bash
# Test Cloud SQL connection
gcloud sql connect cybershield-db --user=postgres

# Check firewall rules
gcloud compute firewall-rules list --filter="name:cloud-sql*"
```

### API Rate Limiting
Gemini API has rate limits. Monitor quota at: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas

## Next Steps

1. Set up automated backups for your database
2. Configure monitoring dashboards in Cloud Monitoring
3. Set up alerts for error rates and performance metrics
4. Implement proper logging and audit trails
5. Schedule regular security reviews

## Support & Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Cloud Firestore Documentation](https://cloud.google.com/firestore/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
