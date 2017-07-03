
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