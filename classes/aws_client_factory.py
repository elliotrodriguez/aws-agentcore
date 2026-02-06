import boto3
from dotenv import dotenv_values

class AwsClientFactory:
    def __init__(self):
        # Load configuration
        config = dotenv_values(".env")
        
        # Create AWS session and assume role
        session = boto3.Session(profile_name=config['AWS_PROFILE'])
        sts = session.client('sts')
        
        # Get temporary credentials
        response = sts.assume_role(
            RoleArn=config['AWS_ROLE_ARN'],
            RoleSessionName='AgentCorePOC_Role'
        )
        
        # Store credentials for all client creations
        self.credentials = response['Credentials']
    
    def create_client(self, clientType):
        client_creator = self._get_client(clientType)
        return client_creator
    
    def _get_client(self, client: str):
        supported_clients = ['sts', 'bedrock', 'bedrock-runtime', 'bedrock-agentcore', 'bedrock-agentcore-control']
        if client in supported_clients:
            return self._create_client(client)
        else:
            raise ValueError(f"Unsupported client type: {client}. Supported: {supported_clients}")
    
    def _create_client(self, client: str):
        return boto3.client(client,                    
                            aws_access_key_id=self.credentials['AccessKeyId'],
                            aws_secret_access_key=self.credentials['SecretAccessKey'],
                            aws_session_token=self.credentials['SessionToken'])



