from azure.storage.queue import QueueService
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
import json


def auth_callack(server, resource, scope):
    credentials =  ServicePrincipalCredentials(
        client_id = config.ApplicationId, #client id
        secret = config.ClientSecret,
        tenant = config.TenantId,
        resource = 'https://vault.azure.net'

    )
    token = credentials.token
    return token['token_type'], token['access_token']

class ConfigurationData(object):
     def __init__(self, j):
         self.__dict__ = json.loads(j)

with open('application.identity', 'r') as myfile:
    secretdata=myfile.read().replace('\n', '')

config = ConfigurationData(secretdata)
print ("Application identity is", config.ApplicationId)

vault_url = "https://xekinadev.vault.azure.net/"
secret_version = ""

client = KeyVaultClient(KeyVaultAuthentication(auth_callack))

piStorageAccountName = client.get_secret(vault_url, "piStorageAccountName", secret_version)
piStorageAccountSecretKey = client.get_secret(vault_url, "piStorageAccountSecretKey", secret_version)
piStorageAccountCameraContainerName = client.get_secret(vault_url, "piStorageAccountCameraContainerName", secret_version)
piStorageAccountPhotoBlobName = client.get_secret(vault_url, "piStorageAccountPhotoBlobName", secret_version)
piStorageAccountCameraStillImagesQueueName = client.get_secret(vault_url, "piStorageAccountCameraStillImagesQueueName", secret_version)

block_blob_service = BlockBlobService(account_name=piStorageAccountName.value, account_key=piStorageAccountSecretKey.value)
block_blob_service.create_container(piStorageAccountCameraContainerName.value)

block_blob_service.create_blob_from_path(
    piStorageAccountCameraContainerName.value,
    piStorageAccountPhotoBlobName.value,
    piStorageAccountPhotoBlobName.value,
    content_settings=ContentSettings(content_type='image/png')
            )
blob_source_url = block_blob_service.make_blob_url(piStorageAccountCameraContainerName.value, piStorageAccountPhotoBlobName.value)

queue_service = QueueService(account_name=piStorageAccountName.value, account_key=piStorageAccountSecretKey.value)
queue_service.create_queue(piStorageAccountCameraStillImagesQueueName.value)
queue_service.put_message(piStorageAccountCameraStillImagesQueueName.value, blob_source_url)

print("Image uploaded:", blob_source_url, "Trigger written to queue:", piStorageAccountCameraStillImagesQueueName.value)