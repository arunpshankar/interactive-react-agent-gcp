# 🚀 Interactive ReAct Agent Client Setup

Follow these steps to get your ReAct Agent client up and running smoothly!

## 🛠️ Run the Client
Launch the client app with Streamlit:

```bash
$ streamlit run client/app.py
```

## 🌐 Configure the API Endpoint

Decide if you want to connect to the remote agent on Google Cloud Run or test it locally.

1. **Using the Remote Agent (Cloud Run)**  
   Set the `AGENT_API_URL` to the deployed endpoint:
   ```python
   AGENT_API_URL = 'https://react-agent-service-390991481152.us-central1.run.app/api/agent'
   ```

2. **Testing Locally**  
   For local testing, use the local server:
   ```python
   # AGENT_API_URL = 'http://localhost:8080/api/agent'
   ```

**Note**: To switch between remote and local, comment out the one you're not using.