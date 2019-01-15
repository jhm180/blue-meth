import http.client, urllib
from google.cloud import storage
import os
from os import path
import base64
import logging
import sys 


def get_rap_file(request):
	# authenticate with Rap server and get ticket 
	creds = urllib.parse.urlencode({'username': '73906', 'password': 'Certs5355'})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPSConnection("technet.rapaport.com")
	conn.request("POST", "/HTTP/Authenticate.aspx", creds, headers)
	response = conn.getresponse()
	auth_ticket = response.read()
	conn.close()
	
	bucket_name = 'rapdvtfiles'
	source_file_name = '/tmp/download.csv'
	destination_blob_name = 'upload.csv'
	
	try:
		# TO DO - Update Filename to include date, upload 
		
		# get file from Rap
		output_file = os.open(source_file_name, os.O_CREAT|os.O_WRONLY)
		params = urllib.parse.urlencode({ 'ticket': auth_ticket })
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = http.client.HTTPConnection("technet.rapaport.com")
		url = "/HTTP/DLS/GetFile.aspx"
		conn.request("POST", url, params, headers)
		response = conn.getresponse()
		logging.warn('response size-' + str(sys.getsizeof(response)))
		data = response.read()
		logging.warn('data size-' + str(sys.getsizeof(data)))
		os.write(output_file, data)
		conn.close()
		
		# upload file to gcloud storage bucket
		storage_client = storage.Client()
		bucket = storage_client.get_bucket(bucket_name)
		blob = bucket.blob(destination_blob_name)
		blob.upload_from_filename(source_file_name)
		output_file.os.close()
		return 'success'
	except IOError:
		output_file = os.open('/tmp/download.csv', os.O_CREAT|os.O_WRONLY)
		output_file.os.close()
		return 'fail' 

