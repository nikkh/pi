import socket
from azure.servicebus import ServiceBusService
from azure.servicebus import Message
import os

print(os.getcwd())

service_namespace='nixpitest'
with open('keys/keys.txt', 'r') as myfile:
    keyval=myfile.read().replace('\n', '')
key_name = 'RootManageSharedAccessKey' # SharedAccessKeyName from Azure portal
key_value = keyval # SharedAccessKey from Azure portal
sbs = ServiceBusService(service_namespace,
                        shared_access_key_name=key_name,
                        shared_access_key_value=key_value)
sbs.create_queue('ippublishqueue')

myip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0],s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) +["no IP found"])[0]
msg = Message(myip)
sbs.send_queue_message('ippublishqueue', msg)
print(myip, 'published to service bus queue')
