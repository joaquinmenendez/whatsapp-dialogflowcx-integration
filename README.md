# WhatsApp-DialogflowCX-Integration

## Description

This repository demonstrates the integration of WhatsApp with Dialogflow CX using Twilio. It allows you to send messages from WhatsApp to a Dialogflow CX agent and receive responses back on WhatsApp.

## Usage

### Prerequisites

* Twilio account with a Sandbox WhatsApp number activated
* Google Cloud Platform (GCP) account with a Dialogflow CX agent configured
* Python environment with the required dependencies installed (see requirements.txt)

### Setup

1. Clone this repository.
2. Set the following environment variables:
    * `accountSID`: Twilio account SID
    * `authToken`: Twilio auth token
    * `projectId`: GCP project ID containing the Dialogflow agent
    * `agentId`: ID of the Dialogflow CX agent
    * `location`: Location of the Dialogflow agent
    * `languageCode`: Language code (ISO format) for the Dialogflow agent

3. Build and Deploy the Cloud Run
   ```bash
   gcloud builds submit --region=us-central1
   ```
### Running the Application locally

1. Configure the Twilio WhatsApp sandbox or your Twilio phone number with the webhook URL of your deployed application:
    ```
    https://YOUR_HOSTNAME/twilio-dialogflowcx
    ```


### Sending and Receiving Messages

* Send a message from WhatsApp to the configured Twilio number.
* The message will be forwarded to the Dialogflow CX agent.
* The agent's response will be returned as a message on WhatsApp.

## Code Structure

* `.gitignore`: Specifies files to ignore in Git.
* `Dockerfile`: Docker configuration for building the application image.
* `cloudbuild.yaml`: Cloud Build configuration file for building and deploying the application.
* `env.yaml`: Contains the environmental variables needed to run the application.
* `gen_ai_services.py`: Contains the `DialogFlowReply` class for interacting with Dialogflow CX.
* `main.py`: Defines the FastAPI application and handles incoming Twilio messages.
* `requirements.txt`: Lists the required Python dependencies.

## License

