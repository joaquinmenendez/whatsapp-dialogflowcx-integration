import os
from typing import MutableSequence
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.cloud.dialogflowcx_v3beta1.types.response_message import ResponseMessage


class DialogFlowReply:
    """
    Encapsulates interactions with a Dialogflow CX agent.
    """

    def __init__(
        self,
        session_id: str,
        project_id: str = None,
        agent_id: str = None,
        location: str = None,
    ):
        """
        Initializes the DialogFlowReply class.

        Args:
            session_id: ID of the Dialogflow CX session to use.
            project_id: ID of the GCP project containing the Dialogflow agent.
                If not provided, attempts to retrieve from the 'projectId' environment variable.
            agent_id: ID of the Dialogflow CX agent.
                If not provided, attempts to retrieve from the 'agentId' environment variable.
            location: Location of the Dialogflow agent.
                If not provided, attempts to retrieve from the 'location' environment variable.
        """
        self.session_id = session_id
        self.project_id = project_id if project_id else os.environ.get("projectId")
        self.agent_id = agent_id if agent_id else os.environ.get("agentId")
        self.location = location if location else os.environ.get("location")
        self.dialogflow_client = self.set_dialogflow_client()
        self.session_path = self.set_session_path()

    def set_dialogflow_client(self):
        """
        Creates and returns a Dialogflow CX SessionsClient.
        """
        return dialogflow.SessionsClient(
            client_options={
                "api_endpoint": f"{self.location}-dialogflow.googleapis.com"
            }
        )

    def set_session_path(self):
        """
        Constructs and returns the session path for the Dialogflow CX session.
        """
        return self.dialogflow_client.session_path(
            project=self.project_id,
            session=self.session_id,
            location=self.location,
            agent=self.agent_id,
        )

    # Create Dialogflow CX request
    def send_request(
        self, message: str, language_code: str
    ) -> MutableSequence[ResponseMessage]:
        """Sends a message to the DialogFlow CX agent and returns the reply.

        Args:
            message: str. The message to send to the agent.
            language_code: str. The language code of the message (e.g., 'en').

        Returns:
            A list of ResponseMessage objects representing the agent's responses.
        """
        request = {
            "session": self.session_path,
            "query_input": {
                "text": {
                    "text": message,
                },
                "language_code": language_code,
            },
        }

        # Get Dialogflow CX response
        try:
            response = self.dialogflow_client.detect_intent(request)
            query_result = response.query_result
            print(f"Dialogflow Request: {query_result.response_messages}")
            if query_result.match and query_result.match.intent:
                print(f"Matched Intent: {query_result.match.intent.display_name}")
            print(f"Current Page: {query_result.current_page.display_name}")
        except Exception as error:
            print(error)
            return []
        return query_result.response_messages
