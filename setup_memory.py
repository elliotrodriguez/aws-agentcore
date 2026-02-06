import uuid
import boto3
from botocore.config import Config
from dotenv import dotenv_values
from classes.aws_client_factory import AwsClientFactory

config = dotenv_values(".env")

factory = AwsClientFactory()
control_client = factory.create_client('bedrock-agentcore-control')
data_client = factory.create_client('bedrock-agentcore')

print("Creating memory resources...\n")

# === SHORT-TERM MEMORY ===
# Only stores raw conversation, no intelligent extraction
stm = control_client.create_memory(
    name=f"Demo_STM_{uuid.uuid4().hex[:8]}",  # Unique name
    memoryStrategies=[],  # Empty = no extraction strategies
    eventExpiryDuration=7  # Keep conversations for 7 days
)

# === LONG-TERM MEMORY ===
# Intelligently extracts preferences and facts
ltm = control_client.create_memory(
    name=f"Demo_LTM_{uuid.uuid4().hex[:8]}",
    memoryStrategies=[
        # Extracts user preferences like "I prefer Python"
        {"userPreferenceMemoryStrategy": {
            "name": "prefs",
            "namespaces": ["/user/preferences/"]
        }},
        # Extracts facts like "My birthday is in January"
        {"semanticMemoryStrategy": {
            "name": "facts",
            "namespaces": ["/user/facts/"]
        }}
    ],
    eventExpiryDuration=30
)
