# this file gets run nightly after the rapnet_import script
# any printed output of this script will be sent to Ollie's email, so try not to use print much

###################
##### LOAD ACTIVE LISTINGS FROM SQL DATABASE & DEFINE SOME GLOBAL VARIABLES
###################

import pandas as pd
import numpy as np
import MySQLdb
c = MySQLdb.connect('localhost', 'root', '3lihu_r007', 'rapnet_listings')
import pandas.io.sql as psql
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab as pl
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
import math
import rapnet_loader as rl

#all_df, current_df, file_date = rl.load_cache()

sql_df = psql.read_frame("""select l.LotNum, l.Owner, convert(l.Price, decimal(10,4)) as PricePerCarat, l.Shape, convert(l.Carat, decimal(10,6)) as Carat, l.Color, l.Clarity, 
l.CutGrade, convert(l.PctRap, decimal(10,6)) as PctRap, l.Cert, convert(l.Depth, decimal(10,6)) as Depth, convert(l.TableWidth, decimal(10,6)) as TableWidth, l.Girdle, 
l.Culet, l.Polish, l.Sym, l.Fluor, l.Meas, l.RapnetComment, l.NumStones, l.CertNum, l.StockNum, l.Make, l.Date, l.City,
l.State, l.Country, l.Image from active_listing l where l.Cert like 'GIA' 
and not l.Color is null and l.Color <> ""
and (l.Color like 'D' or l.color like 'E' or l.color like 'F' or l.color like 'G' or l.color like 'H' or l.color like 'I' or l.color like 'J'\
 or l.color like 'K' or l.color like 'L' or l.color like 'M')
and (l.Clarity like 'IF' or l.Clarity like 'VVS1' or l.Clarity like 'VVS2' or l.Clarity like 'VS1' or l.Clarity like 'VS2' or l.Clarity like 'SI1' \
 or l.Clarity like 'SI2' or l.Clarity like 'SI3' or l.Clarity like 'I1' or l.Clarity like 'I2' or l.Clarity like 'I3')
and not l.Clarity is null and l.Clarity <> ""
and not l.Polish is null and l.Polish <> ''
and not l.Sym is null and l.Sym <> ''
and not l.Fluor is null and l.Fluor <> ''
and not l.Price is null and l.Price <> ''""", c, index_col = 'LotNum')

df['TotalPrice'] = df['Price'] * df['Carat'] #l.Price represents price per carat

all_countries = ['USA', 'Canada', 'United Kingdom', 'Hong Kong', 'India', 'Belgium', 'Israel', 'Sri Lanka', 'Germany', \
            'Thailand', 'UAE', 'China', 'South Africa', 'New Zealand', 'Australia', 'France', 'Singapore', 'Italy', 'Uzbekistan', 'Uganda'] 
usa_only = ['USA']

colors = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
clars = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'SI3', 'I1', 'I2', 'I3']
colors_plot = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
clars_plot = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1']
coffee_pot_colors = ['F', 'G', 'H', 'I', 'J']
coffee_pot_clars = ['VS1', 'VS2', 'SI1', 'SI2']

fluor_faint = ['Faint ', 'Faint Blue', 'Slight', 'Very Slight ', 'Slight Blue', 'Very Slight Blue'] #Do NOT delete spaces at end of items in this list
fluor_none = ['None '] #Do NOT delete spaces at end of items in this list
fluor_medium = ['Medium ', 'Medium Blue', 'Medium Yellow'] #Do NOT delete spaces at end of items in this list
fluor_strong = ['Strong ', 'Strong Blue', 'Very Strong Blue', 'Very Strong '] #Do NOT delete spaces at end of items in this list
fluors = ['Faint ', 'Faint Blue', 'Slight', 'Very Slight ', 'Slight Blue', 'Very Slight Blue', 'None ']

clar_line_colors = {'IF' : 'r' , 'VVS1' : 'g', 'VVS2' : 'b', 'VS1' :'c', 'VS2' : 'm', 'SI1': 'y', 'SI2': 'k', 'I1': 'r', 'I2' : 'g'}
color_line_colors = {'D' : 'r' , 'E' : 'g', 'F' : 'b', 'G' :'c', 'H' : 'm', 'I' : 'y', 'J': 'k', 'K': 'r', 'L' : 'g', 'M' : 'b'}


###################
##### EMBIGGEN DF - ADD NEW COLUMN WITH A KEY, LOAD RAP PRICE LIST, THEN ADD NEW COLUMN AND POUPLATE COLUMN WITH RAP PRICE USING KEY 
###################

shape = 'Round'
fluor = 'None '
color = 'E'
clar = 'VVS2'
cut = 'Excellent'
pol = 'Excellent'
sym = 'Excellent'
cert = 'GIA'
wght_min = .23
wght_max = .29

sql_df_sub = sql_df[\
			 (sql_df['Shape'] == shape) & \
			 (sql_df['Carat'] >= wght_min) & \
			 (sql_df['Carat'] <= wght_max) & \
			 (sql_df['Fluor'] == fluor) & \
			 (sql_df['Color'] == color) & \
			 (sql_df['Clarity'] == clar) & \
			 (sql_df['CutGrade'] == cut) & \
			 (sql_df['Polish'] == pol) & \
			 (sql_df['Sym'] == sym) & \
			 (sql_df['Cert'] == cert)
 			 ]

current_df_sub = current_df[\
			 (current_df['Shape'] == shape) & \
			 (current_df['Carat'] >= wght_min) & \
			 (current_df['Carat'] <= wght_max) & \
			 (current_df['Fluor'] == fluor) & \
			 (current_df['Color'] == color) & \
			 (current_df['Clarity'] == clar) & \
			 (current_df['Cut Grade'] == cut) & \
			 (current_df['Polish'] == pol) & \
			 (current_df['Sym'] == sym) & \
			 (current_df['Cert'] == cert)			 
 			 ]


writer = pd.ExcelWriter('/home/oliver/Dropbox/whitepine/sqlvspandaspickle.xlsx')
sql_df_sub.to_excel(writer, 'sql_df_sub')
current_df_sub.to_excel(writer, 'current_df_sub')
writer.save()
