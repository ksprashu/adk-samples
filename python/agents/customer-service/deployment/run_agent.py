
import argparse
import logging
import sys

import vertexai
from customer_service.config import Config
from vertexai import agent_engines

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

configs = Config()

vertexai.init(
    project=configs.CLOUD_PROJECT,
    location=configs.CLOUD_LOCATION,
)

parser = argparse.ArgumentParser(description="Interact with a deployed agent")
parser.add_argument(
    "--resource_id",
    required=True,
    action="store",
    dest="resource_id",
    help="The resource id of the agent in the format projects/PROJECT_ID/locations/LOCATION/reasoningEngines/REASONING_ENGINE_ID",
)
args = parser.parse_args()

remote_app = agent_engines.get(args.resource_id)

session = remote_app.create_session(user_id="123")
logger.info(f"Created session: {session['id']}")
logger.info("Chat with the agent (type 'exit' to quit):")

while True:
    message = input("> ")
    if message.lower() == "exit":
        break
    
    for event in remote_app.stream_query(
        user_id="123",
        session_id=session["id"],
        message=message,
    ):
        if event.get("content", None):
            print(event["content"], end="")
    print()
