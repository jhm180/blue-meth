import pandas as pd
from os import path
import glob
import re
from datetime import datetime,date,timedelta
from pandas.io.parsers import read_csv
import numpy as np
from itertools import repeat
import sys
import traceback
import gc
from pandas.io.pytables import HDFStore
import shutil
from scipy import stats
import rapnet_loader as rl

###################################################
###### DEFINE GROUPS AND SET KEY VALUES
###################################################

gd_plus = ['Excellent', 'Very Good', 'Good']
fluor_faint = ['Faint ', 'Faint Blue', 'Slight', 'Very Slight ', 'Slight Blue', 'Very Slight Blue'] #Do NOT delete spaces at end of items in this list
fluor_none = ['None '] #Do NOT delete spaces at end of items in this list
fluor_medium = ['Medium ', 'Medium Blue', 'Medium Yellow'] #Do NOT delete spaces at end of items in this list
fluor_strong = ['Strong ', 'Strong Blue', 'Very Strong Blue', 'Very Strong ']


fluor_tags = ['None', 'Faint', 'Medium', 'Strong and VST']
fluors = ['Faint ','Faint', 'Faint Blue', 'Slight', 'Very Slight ', 'Slight Blue', 'Very Slight Blue', 'None', 'None ','Medium ', 'Medium Blue', 'Medium Yellow', 'Strong ', 'Strong Blue', 'Very Strong Blue', 'Very Strong ']

colors = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
clars = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2']

start_time = datetime.now()
last_step_end = datetime.now()
sell_lag = 32 #Sets number of days something has been removed from rapnet before we consider it sold
start_date = datetime(2013, 3, 3) #First day we started downloading market data def get_first(grp):

date_to_extract = datetime(2013, 7, 17)

###################################################
###### Some Functions
###################################################

def get_last(grp):
    grp.sort(columns='event_day', inplace=True, ascending = False)
    return grp.iloc[0]

def days_to_sell(row):
    if row['event_type_first_event'] == 1 and row['event_type_last_event'] == 2 and row['event_day_last_event'] < (datetime.now()-timedelta(days=sell_lag)):
        return (row['event_day_last_event'] - row['event_day_first_event']).days
    else:
        return np.nan

def weight_tag(carat):
    if carat >= 0.23 and carat <= 0.29:
        return 'r023'
    elif carat >= 0.30 and carat <= 0.34:
        return 'r030'
    elif carat >= 0.35 and carat <= 0.39:
        return 'r035'
    elif carat >= 0.40 and carat <= 0.44:
        return 'r040'
    elif carat >= 0.45 and carat <= 0.49:
        return 'r045'
    elif carat >= 0.50 and carat <= 0.54:
        return 'r050'
    elif carat >= 0.55 and carat <= 0.59:
        return 'r055'
    elif carat >= 0.60 and carat <= 0.64:
        return 'r060'
    elif carat >= 0.65 and carat <= 0.69:
        return 'r065'
    elif carat >= 0.70 and carat <= 0.74:
        return 'r070'
    elif carat >= 0.75 and carat <= 0.79:
        return 'r075'
    elif carat >= 0.80 and carat <= 0.84:
        return 'r080'
    elif carat >= 0.85 and carat <= 0.89:
        return 'r085'
    elif carat >= 0.90 and carat <= 0.94:
        return 'r090'
    elif carat >= 0.95 and carat <= 0.99:
        return 'r095'
    elif carat == 1.00:
        return 'r100'
    elif carat == 1.01:
        return 'r101'
    elif carat == 1.02:
        return 'r102'
    elif carat == 1.03:
        return 'r103'
    elif carat == 1.04:
        return 'r104'
    elif carat >= 1.05 and carat <= 1.09:
        return 'r105'
    elif carat >= 1.10 and carat <= 1.19:
        return 'r110'
    elif carat >= 1.20 and carat <= 1.29:
        return 'r120'
    elif carat >= 1.30 and carat <= 1.39:
        return 'r130'
    elif carat >= 1.40 and carat <= 1.49:
        return 'r140'
    elif carat >= 1.50 and carat <= 1.74:
        return 'r150'
    elif carat >= 1.75 and carat <= 1.99:
        return 'r175'
    elif carat >= 2.00 and carat <= 2.24:
        return 'r200'
    elif carat >= 2.25 and carat <= 2.49:
        return 'r225'
    else:
        pass

all_df, current_df, file_date = rl.load_cache()

reindex_all_df = all_df.reset_index()
reindex_all_df['CertNum'] = reindex_all_df['CertNum'].str.replace('*', '')
reindex_all_df = reindex_all_df.set_index(['Owner','CertNum'])

sub_df = reindex_all_df[(reindex_all_df['Carat'] >= 0.23) \
                     & (reindex_all_df['Carat'] <= 0.29) \
                     & (reindex_all_df['Cut Grade'] == 'Excellent') \
                     & (reindex_all_df['Sym'] == 'Excellent') \
                     & (reindex_all_df['Polish'] == 'Excellent') \
                     & (reindex_all_df['Cert'] == 'GIA') \
                     #& (reindex_all_df['Country'] == 'USA') \
                     #& (reindex_all_df['City'] == 'New York') \
                     & (reindex_all_df['Color'].isin(colors)) \
                     & (reindex_all_df['Clarity'].isiin(clars)) \
                     #& (reindex_all_df['Color'].isin(colors)) \
                     #& (reindex_all_df['Clarity'].isin(clars)) \
                     #& (reindex_all_df['LotNum'] == 40422351) \
                     & (reindex_all_df['Fluor'] == 'None ') \
                     & (reindex_all_df['event_day'] <= date_to_extract) \
                     ]


last_entry = sub_df.groupby(level=['Owner','CertNum']).apply(get_last)
    #last_entry[last_entry['event_type'] != 2].to_csv('/home/oliver/Dropbox/whitepine/test.csv')

