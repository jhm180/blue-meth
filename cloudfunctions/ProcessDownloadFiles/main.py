import pandas as pd
# from pandas.io.parsers import read_csv
import numpy as np
from google.cloud import storage
import sys
import os
import logging
import csv


# DONE 
# load data in dataframe
# filter rows - remove GIAs and bad certs
# strip unnecssary columns
# store in bucket 


# TODO
# manage filenames
# rename columns? 
# strip bad certs

def filter_csv(request):
	# set some config values
	unfiltered_filename = 'upload.csv'
	unfiltered_bucket_name = 'rapdvtfiles'
	filtered_filename = 'filtered.csv'
	filtered_bucket_name = 'filtereddvtfiles'
	tmp_filename = '/tmp/download.csv'
	bad_certs = ['123456789', '', '1234567890', '0']
	source_file_name = '/tmp/upload.csv'
	destination_blob_name = 'upload.csv'
	gia = 'GIA'
	data_types = {
		'Diamond ID': 'int64',
		'Depth Percent': 'float64',
		'Supplier country': 'category',
		'Table Percent': 'float64',
		'Date Updated': 'object',
		'State': 'category',
		'City': 'category',
		'Culet Size': 'category',
		'Culet': 'object',
		'Girdle': 'category',
		'Table': 'object',
		'Depth': 'object',
		'Price Percentage': 'float64',
		'Price Per Carat': 'float64',
		'Stock Number': 'object',
		'Certificate Number': 'object',
		'Lab': 'category',
		'Meas Depth': 'float64',
		'Meas Width': 'float64',
		'Meas Length': 'float64',
		'Measurements': 'object',
		'Fluorescence Intensity': 'category',
		'Fluorescence Color': 'category',
		'Symmetry': 'category',
		'Polish': 'category',
		'Cut': 'category',
		'Clarity': 'category',
		'Color': 'category',
		'Weight': 'float64',
		'Shape': 'category',
		'Name Code': 'category',
		'RapNet Account ID': 'int64',
		'Seller Name': 'category'
	}
	cols = [
		'Diamond ID',
		'Depth Percent',
		'Supplier country',
		'Table Percent',
		'Date Updated',
		'State',
		'City',
		'Culet Size',
		'Culet',
		'Girdle',
		'Table',
		'Depth',
		'Price Percentage',
		'Price Per Carat',
		'Stock Number',
		'Certificate Number',
		'Lab',
		'Meas Depth',
		'Meas Width',
		'Meas Length',
		'Measurements',
		'Fluorescence Intensity',
		'Fluorescence Color',
		'Symmetry',
		'Polish',
		'Cut',
		'Clarity',
		'Color',
		'Weight',
		'Shape',
		'Name Code',
		'RapNet Account ID',
		'Seller Name'
	]

	# download raw file, load into dataframe, toss file to save memory
	client = storage.Client()
	bucket = client.get_bucket(unfiltered_bucket_name)
	data = bucket.get_blob(unfiltered_filename)
	csv = data.download_to_filename(tmp_filename)
	df = pd.read_csv(tmp_filename, dtype=data_types, usecols=cols)
	os.remove(tmp_filename)
	#return str(df.info(memory_usage='deep'))

	# filter rows out of df
	df = df.query('Lab == @gia') 
	
	# create, write to, and upload new csv
	df.to_csv(source_file_name)
	bucket = client.get_bucket(filtered_bucket_name)
	blob = bucket.blob(destination_blob_name)
	blob.upload_from_filename(source_file_name)
	
	return 'success' 

