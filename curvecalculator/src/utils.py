import smtplib, ssl
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import pandas as pd
import numpy as np
import math
from google.cloud import storage
import sys
from datetime import datetime


def file_date_output():
    return datetime.today().strftime("%Y-%m-%d")

def get_gcloud_file(bucket_name, file_name):
	tmp_filename = '/tmp/download.csv'
	client = storage.Client()
	bucket = client.get_bucket(bucket_name)
	data = bucket.get_blob(file_name)
	data.download_to_filename(tmp_filename)
	return tmp_filename

def upload_to_gcloud(bucket_name, file_loc, upload_name):
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(upload_name)
	blob.upload_from_filename(file_loc)

def send_email(receiver_email, message):
	port = 465  # For SSL
	#smtp_server = "smtp.gmail.com" 
	sender_email = "whitepinedvt@gmail.com"  # TODO: Move to ENV file. 
	password = "Wpdvt123!@#" # TODO: Move to ENV file. 
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com" , 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)

def stop_server():
	project = 'wpdvt-228113'  # TODO: Move to ENV file. 
	zone = 'us-east1-b'  # TODO: Move to ENV file. 
	instance = 'curvecalc'  # TODO: Move to ENV file. 
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('compute', 'v1', credentials=credentials)
	request = service.instances().stop(project=project, zone=zone, instance=instance)
	response = request.execute()

def ratio(measurement):
    if pd.isnull(measurement):
        return -999999
    measurementx = (measurement.replace('-','x'))
    dims = (measurementx.split('x'))
    side1 = float(dims[0])
    side2 = float(dims[1])
    if side1 == 0 or side2 == 0:
        return -999999
    else:
        return max(side1/side2, side2/side1)

def grade_princess_cuts(df, df_p, mindepth, maxdepth, maxratio, sym, polish, grade):
    df_i = df_p[(df_p['Depth Percent'] >= mindepth) 
               & (df_p['Depth Percent'] <= maxdepth) 
               & (df_p.Ratio <= maxratio) 
               & (df_p.Symmetry.isin(sym)) 
               & (df_p.Polish.isin(polish)) 
               ]
    df.loc[df_i.index, 'Cut'] = grade

def rap_price_key(wt):
    if wt >= 0.01 and wt <= 0.03:
        return 0.01
    elif wt >= 0.04 and wt <= 0.07:
        return 0.07
    elif wt >= 0.08 and wt <= 0.14:
        return 0.08
    elif wt >= 0.15 and wt <= 0.17:
        return 0.15
    elif wt >= 0.18 and wt <= 0.22:
        return 0.18
    elif wt >= 0.23 and wt <= 0.29:
        return 0.23
    elif wt >= 0.30 and wt <= 0.39:
        return 0.30
    elif wt >= 0.40 and wt <= 0.49:
        return 0.40
    elif wt >= 0.50 and wt <= 0.69:
        return 0.50
    elif 0.70 <= wt and wt <= 0.89:
        return 0.70
    elif 0.90 <= wt and wt <= 0.99:
        return 0.90
    elif 1.00 <= wt and wt <= 1.49:
        return 1.00
    elif 1.50 <= wt and wt <= 1.99:
        return 1.50
    elif 2.00 <= wt and wt <= 2.99:
        return 2.00
    elif 3.00 <= wt and wt <= 3.99:
        return 3.00
    elif 4.00 <= wt and wt <= 4.99:
        return 4.00
    elif 5.00 <= wt and wt <= 9.99:
        return 5.00
    elif 10.00 <= wt:
        return 10.00
    else:
        return -999999.0

def shape_disc_key(wt):
    if wt >= 0.01 and wt <= 0.03:
        return 0.01
    elif wt >= 0.04 and wt <= 0.07:
        return 0.04
    elif wt >= 0.08 and wt <= 0.14:
        return 0.08
    elif wt >= 0.15 and wt <= 0.17:
        return 0.15
    elif wt >= 0.18 and wt <= 0.22:
        return 0.18
    elif wt >= 0.23 and wt <= 0.29:
        return 0.23
    elif wt >= 0.30 and wt <= 0.39:
        return 0.30
    elif wt >= 0.40 and wt <= 0.49:
        return 0.40
    elif wt >= 0.50 and wt <= 0.59:
        return 0.50
    elif wt >= 0.60 and wt <= 0.69:
        return 0.60
    elif 0.70 <= wt and wt <= 0.79:
        return 0.70
    elif 0.80 <= wt and wt <= 0.89:
        return 0.80
    elif 0.90 <= wt and wt <= 0.99:
        return 0.90
    elif 1.00 <= wt and wt <= 1.24:
        return 1.00
    elif 1.25 <= wt and wt <= 1.49:
        return 1.25
    elif 1.50 <= wt and wt <= 1.74:
        return 1.50
    elif 1.75 <= wt and wt <= 1.99:
        return 1.75
    elif 2.00 <= wt and wt <= 2.49:
        return 2.00
    elif 2.50 <= wt and wt <= 2.99:
        return 2.50
    elif 3.00 <= wt and wt <= 3.99:
        return 3.00
    elif 4.00 <= wt and wt <= 4.99:
        return 4.00
    elif 5.00 <= wt and wt <= 9.99:
        return 5.00
    elif 10.00 <= wt:
        return 10.00
    else:
        return -999999.0

def rap_shape_key(shape):
    if shape == 'Round':
        return 'BR'
    else:
        return 'PS'

def discount_shape_key(shape):
    if shape == 'Round':
        return 'RB'
    elif shape == 'Princess':
        return 'PR'
    else:
        return 'NA'

def depth_diff(depth):
    if depth >= 72.0:
        return depth - 72.0
    elif depth < 64:
        return 64 - depth
    else:
        return 0

def ratio_diff(ratio):
	# comment
    return math.fabs(ratio - 1)

def grade_rank(grade):
    if pd.isnull(grade):
        return -999999
    if grade == 'Excellent':
        return 0
    elif grade == 'Very Good':
        return 1
    elif grade == 'Good':
        return 2
    elif grade == 'Fair':
        return 3
    elif grade == 'Poor':
        return 4
    else:
        return -999999    
    
def price_curve_key(wt):
    if wt >= 0.01 and wt <= 0.03:
        return 'r01'
    elif wt >= 0.04 and wt <= 0.07:
        return 'r04'
    elif wt >= 0.08 and wt <= 0.14:
        return 'r08'
    elif wt >= 0.15 and wt <= 0.17:
        return 'r15'
    elif wt >= 0.18 and wt <= 0.22:
        return 'r18'
    elif wt >= 0.23 and wt <= 0.29:
        return 'r23'
    elif wt >= 0.30 and wt <= 0.39:
        return 'r30'
    elif wt >= 0.40 and wt <= 0.49:
        return 'r40'
    elif wt >= 0.50 and wt <= 0.59:
        return 'r50'
    elif 0.60 <= wt and wt <= 0.69:
        return 'r60'
    elif 0.70 <= wt and wt <= 0.79:
        return 'r70'
    elif 0.80 <= wt and wt <= 0.89:
        return 'r80'
    elif 0.90 <= wt and wt <= 0.99:
        return 'r90'
    elif 1.00 <= wt and wt <= 1.49:
        return 'rc1'
    elif 1.50 <= wt and wt <= 1.99:
        return 'rcr'
    elif 2.00 <= wt and wt <= 2.99:
        return 'rc2'
    elif 3.00 <= wt and wt <= 3.99:
        return 'rc3'
    elif 4.00 <= wt and wt <= 4.99:
        return 'rc4'
    elif 5.00 <= wt and wt <= 9.99:
        return 'rc5'
    elif 10.00 <= wt:
        return 'rct'
    else:
        return -999999.0

