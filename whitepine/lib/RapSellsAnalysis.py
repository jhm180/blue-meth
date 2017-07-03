
###################################################
###### IMPORT LIBRARIES
###################################################

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
###### DEFINE SOME FUNCTIONS
###################################################

def sale_stats(row):
    add_date = row['event_day_first_event']
    sale_date = row['event_day_last_event']
    fluor_tag = row['Fluor Tag']
    last_price = row['TotalPrice_last_event']
    colclargroup = row['Group Tag']
    weightbin = row['Weight Tag']
    stone_color = row['Color']
    stone_clarity = row['Clarity']
 
    active_comps = filtered_df[\
    (filtered_df['Fluor Tag'] == fluor_tag) & \
    (filtered_df['Color'] == stone_color) & \
    (filtered_df['Clarity'] == stone_clarity) & \
    (filtered_df['Weight Tag'] == weightbin) & \
    (filtered_df['event_day'] <= sale_date)\
    ]
 
    comps_last = active_comps.groupby(level=['Owner','CertNum']).apply(get_last)
    
    if len(comps_last) > 2: 
        comps_last_no_sales = comps_last[(comps_last['event_type'] != 2) & (comps_last['TotalPrice'] > 0)]
        if len(comps_last_no_sales) > 2:
            inventory_num_stones = len(comps_last_no_sales)
            pile_active = stats.percentileofscore(comps_last['TotalPrice'],last_price,kind='mean')
            inventory_value = np.sum(comps_last['TotalPrice'])
            comps_last_NYC = comps_last_no_sales[comps_last_no_sales['City'] == 'New York']
            #comps_last_NYC = comps_last
            if len(comps_last_NYC) > 2:
                inventory_num_stones_NYC = len(comps_last_NYC)
                pile_active_NYC = stats.percentileofscore(comps_last_NYC['TotalPrice'],last_price, kind='mean')
                inventory_value_NYC = np.sum(comps_last['TotalPrice'])
            else:
                inventory_num_stones_NYC = np.nan
                pile_active_NYC = np.nan
                inventory_value_NYC = np.nan
        else:
            inventory_num_stones = np.nan
            pile_active = np.nan
            inventory_value = np.nan
            inventory_num_stones_NYC = np.nan
            pile_active_NYC = np.nan
            inventory_value_NYC = np.nan
    else:
        inventory_num_stones = np.nan
        pile_active = np.nan
        inventory_value = np.nan    
        inventory_num_stones_NYC = np.nan
        pile_active_NYC = np.nan
        inventory_value_NYC = np.nan

    return pd.Series({'Num Stones in Inventory at Sale' : np.nan})
    #return pd.Series({'Num Stones in Inventory at Sale' : inventory_num_stones, \
    #    'Inventory Value at Sale' : inventory_value, \
    #    'Price Percentile at Sale' : pile_active, \
    #    'Num Stones in NYC at Sale' : inventory_num_stones_NYC, \
    #    'NYC Inventory Value at Sale' : inventory_value_NYC, \
    #    'NYC Price Percentile at Sale' : pile_active_NYC \
    #    })


def get_first(grp):
    grp.sort(columns='event_day', inplace=True, ascending = False)
    return grp.iloc[-1]

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

def fluor_tag(fluor):
    if fluor in fluor_none:
        return 'fluor_none'
    if fluor in fluor_faint:
        return 'fluor_faint'
    if fluor in fluor_medium:
        return 'fluor_medium'
    if fluor in fluor_strong:
        return 'fluor_strong'
    else:
        pass

def group_tag(row):
    if row['Color'] in ['D'] and row['Clarity'] in ['IF', 'VVS1', 'VVS2']:
        return 'D-D_IF-VVS2'
    if row['Color'] in ['D'] and row['Clarity'] in ['VS1','VS2']:
        return 'D-D_VS1-VS2'
    if row['Color'] in ['D'] and row['Clarity'] in ['SI1','SI2']:
        return 'D-D_SI1-SI2'
    if row['Color'] in ['E', 'F'] and row['Clarity'] in ['IF', 'VVS1', 'VVS2']:
        return 'E-F_IF-VVS2'
    if row['Color'] in ['E', 'F'] and row['Clarity'] in ['VS1','VS2']:
        return 'E-F_VS1-VS2'
    if row['Color'] in ['E', 'F'] and row['Clarity'] in ['SI1','SI2']:
        return 'E-F_SI1-SI2'
    if row['Color'] in ['G', 'H', 'I'] and row['Clarity'] in ['IF', 'VVS1', 'VVS2']:
        return 'G-I_IF-VVS2'
    if row['Color'] in ['G', 'H', 'I'] and row['Clarity'] in ['VS1','VS2']:
        return 'G-I_VS1-VS2'
    if row['Color'] in ['G', 'H', 'I'] and row['Clarity'] in ['SI1','SI2']:
        return 'G-I_SI1-SI2'
    if row['Color'] in ['J', 'K'] and row['Clarity'] in ['IF', 'VVS1', 'VVS2']:
        return 'J-K_IF-VVS2'
    if row['Color'] in ['J', 'K'] and row['Clarity'] in ['VS1','VS2']:
        return 'J-K_VS1-VS2'
    if row['Color'] in ['J', 'K'] and row['Clarity'] in ['SI1','SI2']:
        return 'J-K_SI1-SI2'
    if row['Color'] in ['L', 'M'] and row['Clarity'] in ['IF', 'VVS1', 'VVS2']:
        return 'L-M_IF-VVS2'
    if row['Color'] in ['L', 'M'] and row['Clarity'] in ['VS1','VS2']:
        return 'L-M_VS1-VS2'
    if row['Color'] in ['L', 'M'] and row['Clarity'] in ['SI1','SI2']:
        return 'L-M_SI1-SI2'
    else:
        pass

def get_percentile(dframe): #old function updated by sale_stats function... delete when sale_stats is tested
    for g in range(len(dframe)):
        if dframe['event_type_first'].iloc[g] == 1 and dframe['event_type_last'].iloc[g] == 2 \
        and dframe['event_day_last'].iloc[g] < (datetime.now()-timedelta(days=sell_lag)):
            sale_date = dframe['event_day_last'].iloc[g]
            add_date = dframe['event_day_first'].iloc[g]
            last_price = dframe['TotalPrice_last'].iloc[g]
            df1 = dframe[(dframe['event_day_first'] < add_date) & (dframe['event_day_last'] < sale_date) & \
                         (dframe['event_type_last'].isin([1,3,4]))]
            return stats.percentileofscore(df1['TotalPrice_last'],last_price)
        else:
            return np.nan

def sale_stats_test(row):
	add_date = row['event_day_first_event']
	sale_date = row['event_day_last_event']
	fluor = row['Fluor Tag']
	last_price = row['TotalPrice_last_event']
	colclargroup = row['Group Tag']
	weightbin = row['Weight Tag']
	active_comps = filtered_df[\
								(filtered_df['Fluor Tag'] == fluor) \
								& (filtered_df['Group Tag'] == colclargroup) \
								& (filtered_df['Weight Tag'] == weightbin) \
								& (filtered_df['event_day'] <= sale_date) \
								]
	return len(active_comps)

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
start_date = datetime(2013, 3, 3) #First day we started downloading market data 


###################################################
###### LOAD DATA
###################################################


all_df, current_df, file_date = rl.load_cache()
# all_df is the whole database, with the event types you see in the above cell
# the index is a multiindex with levels ('event_type','Owner','CertNum,'event_day')
#this gets the latest removals:
#prev_removals = all_df.xs(rl.REMOVE, level='event_type').


print 'Cache Loading Took | %s' %(datetime.now() - last_step_end)
print 'Total Run Time | %s' %(datetime.now() - start_time)
last_step_end = datetime.now()

###################################################
###### FILTER ALL DF DOWN TO WHAT WE'RE FOCUSED ON ---- 
###################################################

filtered_df = all_df[(all_df['Carat'] >= 0.29) \
                     & (all_df['Carat'] <= 2.99) \
                     & (all_df['Cut Grade'].isin(gd_plus)) \
                     & (all_df['Sym'].isin(gd_plus)) \
                     & (all_df['Polish'].isin(gd_plus)) \
                     & (all_df['Cert'] == 'GIA') \
                     & (all_df['Country'] == 'USA') \
                     #& (all_df['City'] == 'New York') \
                     #& (all_df['Color'] == 'E') \
                     #& (all_df['Clarity'] =='VVS1') \
                     & (all_df['Color'].isin(colors)) \
                     & (all_df['Clarity'].isin(clars)) \
                     #& (all_df['LotNum'] == 40422351) \
                     & (all_df['Fluor'].isin(fluors)) \
                     ]

filtered_df = filtered_df.reset_index()
filtered_df['CertNum'] = filtered_df['CertNum'].str.replace('*', '')
filtered_df = filtered_df.set_index(['Owner','CertNum'])
filtered_df['TotalPrice'] = filtered_df['Price'] * filtered_df['Carat']
filtered_df['Group Tag'] = filtered_df.apply(group_tag, axis = 1)
filtered_df['Weight Tag'] = filtered_df['Carat'].apply(weight_tag)
filtered_df['Fluor Tag'] = filtered_df['Fluor'].apply(fluor_tag)

filtered_df.sort(columns='event_day')

print 'Filtering and Tagging Took | %s' %(datetime.now() - last_step_end)
print 'Total Run Time | %s' %(datetime.now() - start_time)
last_step_end = datetime.now()

###################################################
###### GENERATE THE SELLS FILE
###################################################

sells = [] 

grouped = filtered_df.groupby(level=['Owner','CertNum'])
last_entry = grouped.apply(get_last)
last_entry = last_entry.drop(['LotNum','Shape','Carat','Color','Clarity','Cut Grade','Cert','Depth','Table','Girdle','Culet','Polish','Sym','Fluor','Meas','Comment','NumStones','StockNum','Make','Date','City','State','Country','Image','Fluor Tag', 'Weight Tag', 'Group Tag'], axis=1)
first_entry = grouped.apply(get_first)
joined = first_entry.join(last_entry, lsuffix='_first_event', rsuffix='_last_event')
joined['days_to_sell'] = joined.apply(days_to_sell, axis = 1)
sells = joined[np.isfinite(joined['days_to_sell'])]
sells = sells[sells['TotalPrice_last_event'] > 0]
sells.to_csv('/home/oliver/Dropbox/whitepine/sells_pre_stats.csv')
sellz = sells.apply(sale_stats, axis=1)
sells = sells.merge(sellz, left_index = True, right_index = True)
sells.to_csv('/home/oliver/Dropbox/whitepine/sells_post_stats.csv')
#grouped.apply(get_last).to_csv('/home/oliver/Dropbox/whitepine/comps.csv')

print 'Generating Sells List Took | %s' %(datetime.now() - last_step_end)
print 'Total Run Time | %s' %(datetime.now() - start_time)
last_step_end = datetime.now()

#sells.to_csv('/home/oliver/Dropbox/whitepine/test.csv')

#print 'Days to Sell Took | %s' %(datetime.now() - last_step_end)
#print 'Total Run Time | %s' %(datetime.now() - start_time)
#last_step_end = datetime.now()

#print 'Grouping and Joining Took | %s' %(datetime.now() - last_step_end)
#print 'Total Run Time | %s' %(datetime.now() - start_time)
#last_step_end = datetime.now()

#print 'Filtered Length | %s' %(len(filtered_df))
#print 'Grouped Length | %s' %(len(grouped))
#print 'Joined Length | %s' %(len(joined))
#print 'Sells Length | %s' %(len(sells))
#print 'First Event | %s' %(min(sells['event_day_first_event']))
#print 'Last Event | %s' %(max(sells['event_day_last_event']))
