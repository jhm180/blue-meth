import pandas as pd
import numpy as np
import pandas.io.sql as psql
# Force matplotlib to not use any Xwindows backend.

from scipy.optimize import curve_fit
import math
import sys

# OLD DEPENDENCIES - PROBABLY DONT'T NEED
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# sys.path.insert(0, '/home/oliver/src/blue-meth/ipynb')
# import pylab as pl
# import rapnet_loader as rl


def filter_csv(filename):

	# set some config values
	unfiltered_filename = 'upload.csv'
	unfiltered_bucket_name = 'rapdvtfiles'
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

	# filter rows out of df
	df = df.query('Lab == @gia') 

	return df

def end_script():
	return 'success'

	