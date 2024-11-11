Here's the revised guide with additional setup instructions, including steps for exporting the `PROJECT_ID` and clarifying prerequisites:

---

# React Agent Service Deployment on Google Cloud Run

This guide covers the steps to build and deploy a Python-based agent service on Google Cloud Run using Docker. The Docker image is created from a `requirements.txt` file, pushed to Google Artifact Registry, and deployed on Cloud Run.

---

## Prerequisites
- **Docker**: Ensure Docker is installed and running. Alternatively, you can use **Vertex AI Workbench**, which comes pre-installed with Docker and `gcloud`.
- **Google Cloud SDK**: Install the Google Cloud SDK and `gcloud` CLI.
- **Google Cloud Project**: Set up a project with billing enabled.

---

## Deployment Steps

### 1. Export the Project ID
Set your Google Cloud project ID as an environment variable to use in commands:
```bash
export PROJECT_ID=your-google-cloud-project-id
```
Verify the export by checking:
```bash
echo $PROJECT_ID
```

### 2. Authenticate with Google Cloud
Log into your Google Cloud account:
```bash
gcloud auth login
gcloud config set project $PROJECT_ID
```

### 3. Configure Docker to Use Google Cloud Credentials
Set up Docker to use Google Cloud as a credential helper:
```bash
gcloud auth configure-docker
```

### 4. Enable Artifact Registry API
Enable the Artifact Registry API to store your Docker images:
```bash
gcloud services enable artifactregistry.googleapis.com
```

### 5. Build the Docker Image
Navigate to the directory with your `Dockerfile` (e.g., `server/`):
```bash
cd server/
```
Build the Docker image:
```bash
docker build -t gcr.io/$PROJECT_ID/react-agent:latest .
```

### 6. Create an Artifact Registry Repository
Create a new Docker repository in Artifact Registry:
```bash
gcloud artifacts repositories create react-agent-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Repository for React Agent"
```

### 7. Tag and Push the Docker Image
Tag the Docker image for Artifact Registry:
```bash
docker tag gcr.io/$PROJECT_ID/react-agent:latest us-central1-docker.pkg.dev/$PROJECT_ID/react-agent-repo/react-agent:latest
```
Authenticate Docker with Artifact Registry:
```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```
Push the Docker image:
```bash
docker push us-central1-docker.pkg.dev/$PROJECT_ID/react-agent-repo/react-agent:latest
```

### 8. Deploy to Cloud Run
Deploy the Docker container to Cloud Run:
```bash
gcloud run deploy react-agent-service \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/react-agent-repo/react-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

---

## Troubleshooting

- **Image Not Found**: Confirm the image exists in Artifact Registry, and re-run `docker push` if needed.
- **Authentication Errors**: Re-authenticate with `gcloud auth configure-docker us-central1-docker.pkg.dev` and verify permissions.
- **Port Configuration**: Ensure the `PORT` in Cloud Run matches the `EXPOSE` command in the Dockerfile (8080 in this example).

> **Note**: Check the Cloud Run logs for detailed error messages or troubleshooting information.

--- 

## Additional Resources

- [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs)
- [Artifact Registry Guide](https://cloud.google.com/artifact-registry)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

---