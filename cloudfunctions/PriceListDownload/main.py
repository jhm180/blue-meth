from google.cloud import storage
import os
import logging
import datetime
import requests


def get_rap_price_list(event,callback):

	source_file_name = '/tmp/download.csv'
	bucket_name = 'rappricelists'
	
	y = datetime.date.today().strftime("%Y")
	m = datetime.date.today().strftime("%m")
	d = datetime.date.today().strftime("%d")
	destination_blob_name = y+'-'+m+'-'+d+'-'+'RapPriceList.csv'

	creds = {'username': '73906', 'password': 'Certs5355'}

	url1 = "https://technet.rapaport.com/HTTP/Prices/CSV2_Round.aspx"
	r1 = requests.post(url1, data = creds)
	data1 = r1.content

	url2 = "https://technet.rapaport.com/HTTP/Prices/CSV2_Pear.aspx"
	r2 = requests.post(url2, data = creds)
	data2 = r2.content

	output_file = os.open(source_file_name, os.O_CREAT|os.O_WRONLY|os.O_APPEND)
	file_headers = str.encode("Shape Code, Clarity, Color, Min Weight, Max Weight, Rap Price, Date \n")


	os.write(output_file, file_headers)
	os.write(output_file, data1)
	os.write(output_file, data2)

	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(destination_blob_name)
	blob.upload_from_filename(source_file_name)
	os.close(output_file)
	return "completed full run"