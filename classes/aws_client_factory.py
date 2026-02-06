import boto3

class AwsClientFactory:
    def create_client(self, clientType, credentials):
        client_creator = self._get_client(clientType, credentials)
        return client_creator 


    def _get_client(self, client: str, credentials):
        supported_clients = ['sts', 'bedrock', 'bedrock-runtime']
        if client in supported_clients:
            return self._create_client(client, credentials)
        else:
            raise ValueError(f"Unsupported client type: {client}. Supported: {supported_clients}")
    
    def _create_client(self, client: str, credentials):
        return boto3.client(client,                    
                            aws_access_key_id=credentials['AccessKeyId'],
                            aws_secret_access_key=credentials['SecretAccessKey'],
                            aws_session_token=credentials['SessionToken'])
    


