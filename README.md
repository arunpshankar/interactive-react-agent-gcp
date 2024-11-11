# Interactive ReAct Agent in GCP

An interactive ReAct agent implemented in Python, featuring a web-based chat interface built with Streamlit. The agent is containerized with Docker, deployed on Google Cloud Run, and communicates with the UI client over HTTP. This project supports multi-turn conversations and visualizes the agent's thought process during interactions.

## Table of Contents

- [Interactive ReAct Agent in GCP](#interactive-react-agent-in-gcp)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Repository Structure](#repository-structure)
  - [Setup and Installation](#setup-and-installation)
    - [Agent Service](#agent-service)
      - [1. Clone the Repository](#1-clone-the-repository)
      - [2. Install Dependencies](#2-install-dependencies)
      - [3. Run the Agent Service Locally](#3-run-the-agent-service-locally)
    - [Client UI](#client-ui)
      - [1. Navigate to the Client Directory](#1-navigate-to-the-client-directory)
      - [2. Install Dependencies](#2-install-dependencies-1)
      - [3. Run the Streamlit App](#3-run-the-streamlit-app)
  - [Usage](#usage)
  - [Deployment](#deployment)
    - [Deploying to Google Cloud Run](#deploying-to-google-cloud-run)
      - [1. Build and Push the Docker Image](#1-build-and-push-the-docker-image)
      - [2. Deploy the Agent Service](#2-deploy-the-agent-service)
      - [3. Update the Client UI](#3-update-the-client-ui)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **ReAct Agent**: Utilizes Wikipedia and Google search tools to answer queries.
- **Web UI**: Streamlit-based chat interface for interacting with the agent.
- **Multi-turn Conversation**: Supports context-aware ongoing conversations.
- **Trace Visualization**: Displays the agent's reasoning steps.
- **Cloud Deployment**: Agent service containerized with Docker and deployed on Google Cloud Run.
- **Decoupled Architecture**: Separates the client UI from the agent service for scalability.

## Architecture

The system consists of two main components:

1. **Agent Service** (`agent_service/`): A Flask application running the ReAct agent, which is deployed on Google Cloud Run.

2. **Client UI** (`client/`): A Streamlit application that serves as the chat interface, running locally on your machine.

They communicate over HTTP, allowing the agent to process queries and return responses along with the thought process.

## Getting Started

### Prerequisites

- **Python** 3.8 or higher
- **Docker** (for containerizing the agent service)
- **Google Cloud SDK** (for deployment)
- **Streamlit** (for the client UI)
- **Git** (for version control)

### Repository Structure

```
react-agent-chat-ui/
├── README.md
├── agent_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── agent_service.py
│   └── src/
│       └── # Agent-related code and modules
├── client/
│   ├── app.py
│   └── requirements.txt
└── LICENSE
```

## Setup and Installation

### Agent Service

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/react-agent-chat-ui.git
cd react-agent-chat-ui/agent_service
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run the Agent Service Locally

```bash
python agent_service.py
```

The agent service will start running at `http://0.0.0.0:8080`.

### Client UI

#### 1. Navigate to the Client Directory

```bash
cd ../client
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run the Streamlit App

```bash
streamlit run app.py
```

The Streamlit UI will open in your default web browser at `http://localhost:8501`.

## Usage

- **Interact with the Agent**: Use the chat interface to send queries to the agent.
- **Multi-turn Conversations**: The agent maintains context between turns.
- **View Agent's Thought Process**: Expand the "Agent's Thought Process" section to see the reasoning steps.

## Deployment

### Deploying to Google Cloud Run

#### 1. Build and Push the Docker Image

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud auth configure-docker

# Set your GCP project ID
PROJECT_ID=your-gcp-project-id

# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/react-agent:latest .

# Push the image to Google Container Registry
docker push gcr.io/$PROJECT_ID/react-agent:latest
```

#### 2. Deploy the Agent Service

```bash
gcloud run deploy react-agent-service \
  --image gcr.io/$PROJECT_ID/react-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

#### 3. Update the Client UI

In `client/app.py`, update the `AGENT_API_URL` to the URL provided by Cloud Run after deployment.

```python
AGENT_API_URL = 'https://react-agent-service-xxxxxxxxxx-uc.a.run.app/api/agent'
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

---

**Code Structure Details:**

### **1. agent_service/**

This directory contains the code for the agent service, which runs the ReAct agent within a Flask application and is containerized using Docker for deployment on Google Cloud Run.

- **Dockerfile**: Instructions for building the Docker image for the agent service.
- **requirements.txt**: Lists the Python dependencies required by the agent service.
- **agent_service.py**: The Flask application that wraps the ReAct agent and exposes it via an API.
- **src/**: Contains the source code for the agent, organized into modules.
  - **agent.py**: Defines the `Agent`, `Tool`, `Message`, and other related classes.
  - **tools/**: Implements the tools the agent can use.
    - **serp.py**: Contains the `SerpAPIClient` class and the `search` function for Google searches.
    - **wiki.py**: Contains the `search` function for Wikipedia searches.
  - **llm/**: Handles interactions with the language model.
    - **gemini.py**: Contains functions to generate responses using the LLM.
  - **config/**: Configuration files and settings.
    - **setup.py**: General configuration settings.
    - **logging.py**: Configures logging.
  - **utils/**: Utility functions.
    - **io.py**: Functions for reading and writing files.
  - **data/**:
    - **input/**: Contains prompt templates, e.g., `react.txt`.
    - **output/**: Contains output files like `trace.txt`.

### **2. client/**

This directory contains the code for the client UI, built with Streamlit.

- **app.py**: The Streamlit application that serves as the chat interface for interacting with the agent.
- **requirements.txt**: Lists the Python dependencies required by the client UI.

### **3. Additional Files**

- **README.md**: Provides an overview of the project, setup instructions, and usage guidelines.
- **LICENSE**: Contains the license information for the project.
- **.gitignore**: Specifies files and directories to be ignored by Git.

---

**Notes on Code Structure:**

- **Modularity**: The code is organized into clear modules, making it easier to maintain and extend.
- **Separation of Concerns**: The agent service and client UI are decoupled, allowing independent development and scaling.
- **Configuration Management**: Configurations are centralized in the `config/` directory.
- **Logging and Error Handling**: Proper logging is implemented to aid in debugging and monitoring.
- **Documentation**: Each module and function includes comments and docstrings for clarity.

---

**Next Steps:**

- **Initialize Git Repository**:

  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin https://github.com/yourusername/react-agent-chat-ui.git
  git push -u origin master
  ```

- **Complete the Code Implementation**: Fill in the code files with the appropriate logic, ensuring all dependencies are met.

- **Testing**: Write unit tests for critical components to ensure reliability.

- **CI/CD Setup**: Consider setting up continuous integration and deployment pipelines using GitHub Actions or another CI/CD tool.

- **Enhancements**:

  - **Authentication**: Secure the agent API with authentication if necessary.
  - **Error Handling in UI**: Improve error handling in the Streamlit app to provide better user feedback.
  - **Scaling**: Explore options for scaling the agent service and client UI for production use.

