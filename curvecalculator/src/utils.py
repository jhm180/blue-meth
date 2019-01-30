import smtplib, ssl
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials




def send_email(receiver_email, message):
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com" 
	sender_email = "whitepinedvt@gmail.com"  # TODO: Move to ENV file. 
	password = "Wpdvt123!@#" # TODO: Move to ENV file. 
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)


def stop_server():
	project = 'wpdvt-228113'  # TODO: Move to ENV file. 
	zone = 'us-east1-b'  # TODO: Move to ENV file. 
	instance = 'shutdown-test'  # TODO: Move to ENV file. 
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('compute', 'v1', credentials=credentials)
	request = service.instances().stop(project=project, zone=zone, instance=instance)
	response = request.execute()