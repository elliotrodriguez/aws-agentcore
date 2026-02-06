import boto3
from dotenv import dotenv_values
from classes.aws_client_factory import AwsClientFactory

config = dotenv_values(".env")

session = boto3.Session(profile_name=config['AWS_PROFILE'])
sts = session.client('sts')
get_temp_creds = sts.assume_role(RoleArn=config['AWS_ROLE_ARN'], RoleSessionName='AgentCorePOC_Role')

temp_creds = get_temp_creds['Credentials']

assumeRoleClient = AwsClientFactory().create_client('sts', temp_creds)
bedrockClient = AwsClientFactory().create_client('bedrock', temp_creds)
bedrockRuntimeClient = AwsClientFactory().create_client('bedrock-runtime', temp_creds)

user_message = "Who won the AL batting title in 1983?"

conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}]
    }
]

response = bedrockRuntimeClient.converse(
    modelId="amazon.nova-lite-v1:0",
    messages=conversation,
    inferenceConfig={"maxTokens": 300, "temperature": 0.5, "topP": 0.9}
)

response_text = response["output"]["message"]["content"][0]["text"]
print(response_text)

