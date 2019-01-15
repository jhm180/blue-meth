#
# Get Authentication Ticket
#
import http.client, urllib
from google.cloud import storage
import os
from os import path
import base64
import logging
import sys 



"""
params = urllib.urlencode({'username': 'omellet', 'password': 'omellet5355'})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = http.client.HTTPSConnection("technet.rapaport.com")
conn.request("POST", "/HTTP/Authenticate.aspx", params, headers)
response = conn.getresponse()
auth_ticket = response.read()
conn.close()
bucket_name = 'https://console.cloud.google.com/storage/browser/rapdvtfiles'
"""

#
# Get the download
#
def hello_get(request):
    return 'Hello World!'

def get_rap_file(request):
	creds = urllib.parse.urlencode({'username': '73906', 'password': 'Certs5355'})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPSConnection("technet.rapaport.com")
	conn.request("POST", "/HTTP/Authenticate.aspx", creds, headers)
	response = conn.getresponse()
	auth_ticket = response.read()
	logging.warn('creds - ' + str(creds))
	logging.warn('auth ticket - ' + str(auth_ticket))
	conn.close()
	bucket_name = 'rapdvtfiles'
	source_file_name = '/tmp/download.csv'
	destination_blob_name = 'upload.csv'
	try:
		# TO DO - Update Filename to include date
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
		storage_client = storage.Client()
		bucket = storage_client.get_bucket(bucket_name)
		blob = bucket.blob(destination_blob_name)
		blob.upload_from_filename(source_file_name)
		output_file.os.close()
		return 'success'
		#storage_client = storage.Client()urllib.parse.urlencode
		#bucket = storage_client.get_bucket(bucket_name)
		#blob = bucket.blob(destination_blob_name)
		#upload_blob(bucket_name, 'download.csv', 'test.csv')
	except IOError:
		output_file = os.open('/tmp/download.csv', os.O_CREAT|os.O_WRONLY)
		output_file.os.close()
		return 'fail' 
"""
		logging.warn('response size-' + str(sys.getsizeof(response)))

		data = response.read()
		logging.warn('data size-' + str(sys.getsizeof(data)))

		data = base64.b64encode(data)
		logging.warn('encoded data size-' + str(sys.getsizeof(data)))

		os.write(output_file, data)
		conn.close()
		# output_file.os.close()
		storage_client = storage.Client()
		bucket = storage_client.get_bucket(bucket_name)
		blob = bucket.blob(destination_blob_name)
		blob.upload_from_filename(source_file_name)
		return 'success'
		#storage_client = storage.Client()
		#bucket = storage_client.get_bucket(bucket_name)
		#blob = bucket.blob(destination_blob_name)
		#upload_blob(bucket_name, 'download.csv', 'test.csv')
"""

"""
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # Uploads a file to the bucket. 
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

#    print('File {} uploaded to {}.'.format(
#        source_file_name,
#        destination_blob_name))

# https://console.cloud.google.com/storage/browser/rapdvtfiles
#import os.path

save_path = 'C:/example/'

name_of_file = raw_input("What is the name of the file: ")

completeName = os.path.join(save_path, name_of_file+".txt")         

file1 = open(completeName, "w")

toFile = raw_input("Write what you want into the field")

file1.write(toFile)

file1.close()
"""