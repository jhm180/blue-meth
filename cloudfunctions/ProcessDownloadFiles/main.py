import pandas as pd
# from pandas.io.parsers import read_csv
import numpy as np
from google.cloud import storage
import sys
import os


# DONE 
# load data in dataframe


# TODO
# filter rows - remove GIAs and bad certs
# strip unnecssary columns
# rename columns? 
# store in bucket 

def filter_csv(request):
	unfiltered_filename = 'upload.csv'
	unfiltered_bucket_name = 'rapdvtfiles'
	filtered_filename = 'filtered.csv'
	filtered_bucket_name = 'filtereddvtfiles'
	tmp_filename = '/tmp/download.csv'
	
	client = storage.Client()
	bucket = client.get_bucket(unfiltered_bucket_name)
	data = bucket.get_blob(unfiltered_filename)
	csv = data.download_to_filename(tmp_filename)

	try: 
		df = pd.read_csv(tmp_filename)
		return str(sys.getsizeof(df))
	except: 
		return 'fail - csv size = '
