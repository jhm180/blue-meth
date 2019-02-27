import os
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


def start_server(data, context):
	project = os.environ.get('VM_PROJECT_ID') 
	zone = os.environ.get('VM_ZONE') 
	server_name = os.environ.get('VM_NAME')
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('compute', 'v1', credentials=credentials)
	request = service.instances().start(project=project, zone=zone, instance=server_name)
	response = request.execute()



