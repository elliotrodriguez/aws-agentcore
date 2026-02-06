import boto3
from dotenv import dotenv_values
from classes.aws_client_factory import AwsClientFactory

config = dotenv_values(".env")

factory = AwsClientFactory()
assumeRoleClient = factory.create_client('sts')
bedrockClient = factory.create_client('bedrock')
bedrockRuntimeClient = factory.create_client('bedrock-runtime')

user_message = "Who won the AL batting title in 1983?"

conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}]
    }
]

response = bedrockRuntimeClient.converse(
    modelId=config["MODEL_ID"],
    messages=conversation,
    inferenceConfig={"maxTokens": 300, "temperature": 0.5, "topP": 0.9}
)

response_text = response["output"]["message"]["content"][0]["text"]
print(response_text)

