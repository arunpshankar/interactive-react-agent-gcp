Thank you for pointing that out. Here’s the revised guide with the step for creating the credentials folder and adding the necessary keys.

---

# Deploying a React Agent Service on Google Cloud Run

This guide provides a comprehensive process to build and deploy a Python-based React Agent service using Docker on Google Cloud Run. The Docker image is created from a `requirements.txt` file, pushed to Google Artifact Registry, and deployed to Cloud Run.

---

## Prerequisites

- **Docker**: Ensure Docker is installed and running. Alternatively, use **Vertex AI Workbench**, which includes Docker and `gcloud`.
- **Google Cloud SDK**: Install the Google Cloud SDK, including the `gcloud` CLI.
- **Google Cloud Project**: Set up a Google Cloud project with billing enabled.

---

## Deployment Steps

### 1. Set Up the Project ID

Export your Google Cloud Project ID as an environment variable:

```bash
export PROJECT_ID=your-google-cloud-project-id
```

Verify the export:

```bash
echo $PROJECT_ID
```

### 2. Authenticate with Google Cloud

Log into your Google Cloud account:

```bash
gcloud auth login
gcloud config set project $PROJECT_ID
```

### 3. Configure Docker with Google Cloud

Set Docker to use Google Cloud credentials:

```bash
gcloud auth configure-docker
```

### 4. Enable the Artifact Registry API

Enable the Artifact Registry API to store Docker images:

```bash
gcloud services enable artifactregistry.googleapis.com
```

### 5. Create a Credentials Folder and Add Keys

Inside your project directory, create a `credentials` folder to store service account and API keys:

```bash
mkdir -p ./server/credentials
```

Place your service account credentials (e.g., `key.json`) and SERP API credentials (e.g., `key.yml`) inside the `./server/credentials` folder. Be sure to add these files to your `.gitignore` to keep them secure:

```plaintext
# Add to .gitignore
server/credentials/key.json
server/credentials/key.yml
```

### 6. Build the Docker Image

Navigate to the directory containing your `Dockerfile` (e.g., `server/`):

```bash
cd server/
```

Build the Docker image:

```bash
docker build -t gcr.io/$PROJECT_ID/react-agent:latest .
```

### 7. Create an Artifact Registry Repository

Create a new Docker repository in Artifact Registry:

```bash
gcloud artifacts repositories create react-agent-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Repository for React Agent"
```

### 8. Tag and Push the Docker Image

Tag the Docker image for Artifact Registry:

```bash
docker tag gcr.io/$PROJECT_ID/react-agent:latest us-central1-docker.pkg.dev/$PROJECT_ID/react-agent-repo/react-agent:latest
```

Push the Docker image:

```bash
docker push us-central1-docker.pkg.dev/$PROJECT_ID/react-agent-repo/react-agent:latest
```

### 9. Deploy the Service to Cloud Run

Deploy the Docker container to Cloud Run:

```bash
gcloud run deploy react-agent-service \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/react-agent-repo/react-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

After deployment, you should see a message like:

```
Service [react-agent-service] revision [react-agent-service-00010-hns] has been deployed and is serving 100 percent of traffic.
Service URL: https://react-agent-service-xxxxxxxxxx.us-central1.run.app
```

Use this Service URL to interact with the deployed agent from your client application.

---

## Troubleshooting

- **Image Not Found**: Ensure the image exists in Artifact Registry and re-run `docker push` if needed.
- **Authentication Errors**: Re-authenticate with `gcloud auth configure-docker us-central1-docker.pkg.dev` and verify permissions.
- **Port Configuration**: Confirm the `PORT` in Cloud Run matches the `EXPOSE` command in the Dockerfile (e.g., 8080 in this example).

> **Tip**: Use Cloud Run logs to view detailed error messages and troubleshoot issues.

To list all images:

```bash
docker images
```

To delete any previous images:

```bash
docker rmi -f <image-id>
```

---

## Additional Resources

- [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs)
- [Artifact Registry Guide](https://cloud.google.com/artifact-registry)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

---