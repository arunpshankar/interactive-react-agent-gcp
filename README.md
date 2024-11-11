# Interactive ReAct Agent in GCP 🚀

An interactive ReAct agent implemented in Python, featuring a web-based chat interface built with Streamlit. The agent is containerized with Docker, deployed on Google Cloud Run, and communicates with the UI client over HTTP. This project supports visualizing the agent's thought process during interactions.

## Features ✨

- **ReAct Agent** 🤖: Utilizes Wikipedia and Google search tools to answer queries.
- **Web UI** 🖥️: Streamlit-based chat interface for interacting with the agent.
- **Trace Visualization** 🔍: Displays the agent's reasoning steps.
- **Cloud Deployment** ☁️: Agent service containerized with Docker and deployed on Google Cloud Run.
- **Decoupled Architecture** 🛠️: Separates the client UI from the agent service for scalability.

## Architecture 🏗️

The system consists of two main components:

1. **Agent Service** (`server/`): A Flask application running the ReAct agent, which is deployed on Google Cloud Run.
2. **Client UI** (`client/`): A Streamlit application that serves as the chat interface, running locally on your machine.

They communicate over HTTP, allowing the agent to process queries and return responses along with the thought process.

## Getting Started ⚙️

### Prerequisites 📋

- **Python** 3.8 or higher
- **Docker** (for containerizing the agent service)
- **Google Cloud SDK** (for deployment)
- **Streamlit** (for the client UI)
- **Git** (for version control)

### Setup Steps

1. **Clone the Repository** 📂

    ```bash
    git clone https://github.com/arunpshankar/react-agent-chat-ui.git
    cd react-agent-chat-ui
    ```

2. **Create a Virtual Environment** 🐍

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install All Requirements** 📦

    ```bash
    pip install -r server/requirements.txt
    pip install -r client/requirements.txt
    ```

4. **Service Account Credentials** 🔑

   Ensure you have your Google Cloud service account credentials ready. Place the JSON credentials file in the project’s root directory and export it:

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
    export PYTHONPATH=$PYTHONPATH:.
    ```

## Running the Project Locally 🌍

### Agent Service

1. **Run the Agent Service**

    Navigate to the `server/` directory and start the agent service:

    ```bash
    cd server
    python app.py
    ```

   The agent service will start running at `http://0.0.0.0:8080`.

### Client UI

1. **Run the Streamlit Client UI**

    From the `client/` directory, start the Streamlit app:

    ```bash
    cd ../client
    streamlit run app.py
    ```

   The Streamlit UI will open in your default web browser at `http://localhost:8501`.

## Deployment 🌐

To deploy the ReAct agent to Google Cloud Run, refer to the deployment instructions in `./server/README.md`. This includes Dockerizing the service and configuring it to run on Google Cloud.