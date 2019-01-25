import http.client, urllib
from google.cloud import storage
import os
from os import path
import logging
import sys 
import datetime


def get_rap_file_v2(event,callback):
	try: 
		# authenticate with Rap server and get ticket 
		creds = urllib.parse.urlencode({'username': '73906', 'password': 'Certs5355'})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = http.client.HTTPSConnection("technet.rapaport.com")
		conn.request("POST", "/HTTP/Authenticate.aspx", creds, headers)
		response = conn.getresponse()
		auth_ticket = response.read()
		conn.close()

		y = datetime.date.today().strftime("%Y")
		m = datetime.date.today().strftime("%m")
		d = datetime.date.today().strftime("%d")
		destination_blob_name = y+'-'+m+'-'+d+'-'+'FullRapFile.csv'
		bucket_name = 'rapdvtfiles'
		source_file_name = '/tmp/download.csv'
		
		# TO DO - email joe if error
		
		# get file from Rap
		output_file = os.open(source_file_name, os.O_CREAT|os.O_WRONLY)
		params = urllib.parse.urlencode({ 'ticket': auth_ticket })
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = http.client.HTTPConnection("technet.rapaport.com")
		url = "/HTTP/DLS/GetFile.aspx"
		conn.request("POST", url, params, headers)
		response = conn.getresponse()
		data = response.read()
		os.write(output_file, data)
		conn.close()
		
		# upload file to gcloud storage bucket
		storage_client = storage.Client()
		bucket = storage_client.get_bucket(bucket_name)
		blob = bucket.blob(destination_blob_name)
		blob.upload_from_filename(source_file_name)
		os.close(output_file)
	except Exception:
		return "Failed to download file from Rap and upload to cloud bucket"

'''
	try: 
		logging.warn('pre auth_key')
		logging.warn('Auth Key type = '+str(type(request.json["auth_key"])))
		auth_key = request.json["auth_key"]
		logging.warn('Auth Key = '+str(auth_key))
		if auth_key != "carsliftdoorhead":
			return  "Invalid authorization key"
		else: 
'''
#	except Exception: 
#		return "JSON body is invalid. JSON must include key value pair for {auth_key : key}"



