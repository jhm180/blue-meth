
###################
##### LOAD ACTIVE LISTINGS FROM SQL DATABASE & DEFINE SOME GLOBAL VARIABLES
###################

import pandas as pd
import numpy as np
import pandas.io.sql as psql 
from scipy.optimize import curve_fit
import math
import sys
from datetime import datetime
import statsmodels.api as sm
from os import path
import os
import openpyxl
import utils
import psycopg2
import math

# TOCHECK - PRINCESS OUTPUT BROKEN - DONE... VERIFY
# TOCHECK - COMPLARE ILOC / IX OUTPUT AFTER FIX   


wp_path = '/tmp/'
all_countries = ['usa', 'canada', 'united kingdom', 'hong kong', 'india', 'belgium', 'israel', 'sri lanka', 'germany', \
            'thailand', 'uae', 'china', 'south africa', 'new zealand', 'australia', 'france', 'singapore', 'italy', 'uzbekistan', 'uganda']
usa_only = ['usa']

colors = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'] 
clars = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'SI3', 'I1', 'I2', 'I3'] 
colors_plot = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'] 
clars_plot = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1'] 
coffee_pot_colors = ['F', 'G', 'H', 'I', 'J']
coffee_pot_clars = ['VS1', 'VS2', 'SI1', 'SI2']

fluor_faint = ['Faint ', 'Faint','Faint Blue', 'Slight', 'Very Slight ', 'Slight Blue', 'Very Slight Blue'] #Do NOT delete spaces at end of items in this list
fluor_none = ['None ', 'None'] #Do NOT delete spaces at end of items in this list
fluor_medium = ['Medium','Medium ', 'Medium Blue', 'Medium Yellow'] #Do NOT delete spaces at end of items in this list
fluor_strong = ['Strong','Strong ', 'Strong Blue', 'Very Strong Blue', 'Very Strong '] #Do NOT delete spaces at end of items in this list
fluors = ['Faint ', 'Faint Blue', 'Slight', 'Very Slight ', 'Slight Blue', 'Very Slight Blue', 'None ']
fluor_none_and_faint = ['None','Faint','None ', 'Faint ', 'Faint Blue', 'Slight', 'Very Slight ', 'Slight Blue', 'Very Slight Blue']

clar_line_colors = {'IF' : 'r' , 'VVS1' : 'g', 'VVS2' : 'b', 'VS1' :'c', 'VS2' : 'm', 'SI1': 'y', 'SI2': 'k', 'I1': 'r', 'I2' : 'g'}
color_line_colors = {'D' : 'r' , 'E' : 'g', 'F' : 'b', 'G' :'c', 'H' : 'm', 'I' : 'y', 'J': 'k', 'K': 'r', 'L' : 'g', 'M' : 'b'}

csv_data_types = { 'Diamond ID': 'int64', 'Depth Percent': 'float64', 'Supplier country': 'category', 'Table Percent': 'float64', 'Date Updated': 'object', 'State': 'category', 'City': 'category', 'Culet Size': 'category', 'Culet': 'object', 'Girdle': 'category', 'Table': 'object', 'Depth': 'category', 'Price Percentage': 'float64', 'Price Per Carat': 'float64', 'Stock Number': 'object', 'Certificate Number': 'object', 'Lab': 'category', 'Meas Depth': 'float64', 'Meas Width': 'float64', 'Meas Length': 'float64', 'Measurements': 'object', 'Fluorescence Intensity': 'object', 'Fluorescence Color': 'category', 'Symmetry': 'object', 'Polish': 'object', 'Cut': 'object', 'Clarity': 'category', 'Color': 'category', 'Weight': 'float64', 'Shape': 'category', 'Name Code': 'category','RapNet Account ID': 'int64', 'Seller Name': 'category' }

csv_columns = ['Diamond ID', 'Depth Percent', 'Supplier country', 'Table Percent', 'Date Updated', 'State', 'City', 'Culet Size', 'Culet', 'Girdle', 'Table', 'Depth', 'Price Percentage', 'Price Per Carat','Stock Number', 'Certificate Number', 'Lab', 'Meas Depth', 'Meas Width', 'Meas Length', 'Measurements', 'Fluorescence Intensity', 'Fluorescence Color', 'Symmetry', 'Polish', 'Cut', 'Clarity', 'Color', 'Weight', 'Shape','Name Code','RapNet Account ID', 'Seller Name']

# grade all princess cuts

def price_curve_generator_all(df, wp_path, file_date):
    output = {\
                'Shape' : [], \
                'Color' : [], \
                'Clarity' : [], \
                'CurveKey' : [], \
                'CurveRangeMin' : [], \
                'CurveRangeMax' : [], \
                'PolyDegree' : [], \
                'Px2' : [], \
                'Px1' : [], \
                'Px0' : [], \
                'StdDev' : [], \
                'NumStones': [], \
                'ResidSlope': [], \
                'ResidCept': [] \
                }
    r01 = np.linspace(0.00, 0.03, 50)
    r04 = np.linspace(0.04, 0.07, 50)
    r08 = np.linspace(0.08, 0.14, 50)
    r15 = np.linspace(0.15, 0.17, 50)
    r18 = np.linspace(0.18, 0.22, 50)
    r23 = np.linspace(0.23, 0.29, 50)
    r30 = np.linspace(0.30, 0.39, 50)
    r40 = np.linspace(0.40, 0.49, 50)
    r50 = np.linspace(0.50, 0.59, 50)
    r60 = np.linspace(0.60, 0.69, 50)
    r70 = np.linspace(0.70, 0.79, 50)
    r80 = np.linspace(0.80, 0.89, 50)
    r90 = np.linspace(0.90, 0.99, 50)
    rc1 = np.linspace(1.00, 1.49, 50)
    rcr = np.linspace(1.50, 1.99, 50)
    rc2 = np.linspace(2.00, 2.99, 50)
    rc3 = np.linspace(3.00, 3.99, 50)
    rc4 = np.linspace(4.00, 4.99, 50)
    rc5 = np.linspace(5.00, 9.99, 50)
    rct = np.linspace(10.00, 29.99, 50)

    rc_bins = [r01, r04, r08, r15, r18, r23, r30, r40, r50, r60, r70, r80, r90, rc1, rcr, rc2, rc3, rc4, rc5, rct]


    shapes = [ \
                ['Princess', ['Excellent'],  ['Excellent', 'Very Good', 'Good'],  ['Excellent', 'Very Good', 'Good'], 'PS', usa_only, 'PR'], \
                ['Round', ['Excellent'],  ['Excellent'],  ['Excellent'], 'BR', all_countries, 'RB'] \
                ]


    df_caratfilt = df[(df.Weight >= 0.23) & (df.Weight < 3.50) & (df['Price Per Carat'] > 0)]
    for z in range(len(shapes)):
        shape = shapes[z][0]
        cutgrade = shapes[z][1]
        polish = shapes[z][2]
        sym = shapes[z][3]
        rap_shape_key = shapes[z][4]
        location = shapes[z][5]
        shape_key = shapes[z][6]

        # hoist common comparisons out of the loops so we only do them once per shape
        df_iter = df_caratfilt[(df_caratfilt['Supplier country'].str.lower().isin(location)) \
        	& (df_caratfilt['Cut'].isin(cutgrade)) \
        	& (df_caratfilt.Polish.isin(polish)) \
        	& (df_caratfilt.Symmetry.isin(sym)) \
        	& (df_caratfilt['Fluorescence Intensity'].isin(fluor_none))]

        #carat_bins = [(1.00, 1.50, 1.00, 1.49, 1.00, 2, 'rc1', rc1)]
        carat_bins = [ \
                  (0.00, 0.04, 0.01, 0.03, 0.01, 1, 'r01', r01),\
                  (0.04, 0.08, 0.04, 0.07, 0.04, 1, 'r04', r04),\
                  (0.08, 0.15, 0.08, 0.14, 0.08, 1, 'r08', r08),\
                  (0.15, 0.18, 0.15, 0.17, 0.15, 1, 'r15', r15),\
                  (0.18, 0.23, 0.18, 0.22, 0.18, 1, 'r18', r18),\
                  (0.23, 0.30, 0.23, 0.29, 0.23, 1, 'r23', r23),\
                  (0.30, 0.40, 0.30, 0.39, 0.30, 1, 'r30', r30),\
                  (0.40, 0.50, 0.40, 0.49, 0.40, 1, 'r40', r40),\
                  (0.50, 0.60, 0.50, 0.59, 0.50, 1, 'r50', r50),\
                  (0.60, 0.70, 0.60, 0.69, 0.50, 1, 'r60', r60),\
                  (0.70, 0.80, 0.70, 0.79, 0.70, 1, 'r70', r70),\
                  (0.80, 0.90, 0.80, 0.89, 0.70, 1, 'r80', r80),\
                  (0.90, 1.00, 0.90, 0.99, 0.90, 1, 'r90', r90),\
                  (1.00, 1.50, 1.00, 1.49, 1.00, 2, 'rc1', rc1),\
                  (1.50, 2.00, 1.50, 1.99, 1.50, 2, 'rcr', rcr),\
                  (2.00, 3.00, 2.00, 2.99, 2.00, 2, 'rc2', rc2),\
                  (3.00, 4.00, 3.00, 3.99, 3.00, 2, 'rc3', rc3),\
                  (4.00, 5.00, 4.00, 4.99, 4.00, 2, 'rc4', rc4),\
                  (5.00, 10.00, 5.00, 9.99, 5.00, 2, 'rc5', rc5),\
                  (10.00, 30.00, 10.00, 29.99, 10.00, 2, 'rct', rct)\
                  ]

        for i in range(len(carat_bins)):
            fxn_min = carat_bins[i][0]
            fxn_max = carat_bins[i][1]
            plot_min = carat_bins[i][2]
            plot_max = carat_bins[i][3]
            rap_price_key = carat_bins[i][4]
            degree = carat_bins[i][5]
            curve_key = carat_bins[i][6]
            plot_linspace = carat_bins[i][7]
            fxn_plus_min = fxn_max # carat_bins[i][1]
            fxn_plus_max = fxn_plus_min + .5 #carat_bins[i][1]+.5


            for color in colors_plot:
                for clar in clars_plot:
                    #create a smaller dataframe with a single combination of color and clarity
                    df_temp = df_iter[ \
                                (df_iter['Shape'] == shape) \
                                & (df_iter['Color'] == color) \
                                & (df_iter['Clarity'] == clar) \
                                ]

                    #break up color/clarity dataframe into smaller chunks based on carat weight
                    df_fxn_range_pre = df_temp[(df_temp['Weight'] >= fxn_min) & (df_temp['Weight'] < fxn_max)]
                    df_fxn_range_plus_pre = df_temp[(df_temp['Weight'] >= fxn_plus_min) & (df_temp['Weight'] < fxn_plus_max)]

                    #get cheapest two stones that weigh more than the current weight bin, append them to the smaller color/clarity dataframe
                    cheapest_n = lambda d, n: d.loc[d.TotalPrice.nsmallest(n).index]
                    if degree == 2:
                        df_fxn_range = pd.concat([df_fxn_range_pre, cheapest_n(df_fxn_range_plus_pre, 2)])
                    elif degree == 1:
                        df_fxn_range = pd.concat([df_fxn_range_pre, cheapest_n(df_fxn_range_plus_pre, 1)])
                    else:
                        df_fxn_range = []
                    #df_fxn_range = pd.concat([df_fxn_range_pre, df_fxn_range_plus[:2]])
                    df_plot_range = df_temp[(df_temp['Weight'] >= plot_min) & (df_temp['Weight'] < plot_max)]


                    #exception handling for certain criteria... exclude small and large stones, exclude lesser clarities, exclude empty categories
                    #exclude categories with only a few stones (minimum stone limits set here are arbitrary)
                    #create dummy entries in the output dictionary for the exlcluded categories
                    if ( \
                        plot_min < .3 \
                        or (plot_min < .5 and shape == 'Princess')
                        or plot_max >= 3.00 \
                        or clar == 'SI3' \
                        or clar == 'I2' \
                        or clar == 'I3' \
                        or len(df_temp) == 0 \
                        or (len(df_fxn_range_pre) <= 4 and degree ==1) \
                        or (len(df_fxn_range) <= 9 and degree ==2) \
                        or len(df_fxn_range) == 0
                        or len(df_plot_range) == 0
                        ):

                        output['Shape'].append(shape_key)
                        output['Color'].append(color)
                        output['Clarity'].append(clar)
                        output['CurveKey'].append(curve_key)
                        output['CurveRangeMin'].append(plot_min)
                        output['CurveRangeMax'].append(plot_max)
                        output['PolyDegree'].append(-999999)
                        output['Px2'].append(-999999)
                        output['Px1'].append(-999999)
                        output['Px0'].append(-999999)
                        output['StdDev'].append(-999999)
                        output['NumStones'].append(len(df_plot_range))
                        output['ResidSlope'].append(-999999)
                        output['ResidCept'].append(-999999)

                    else:
                        #calculate fit parameters for best fit polynomial curve
                        fit_params = np.poly1d(np.polyfit(df_fxn_range['Weight'],df_fxn_range['TotalPrice'], degree, full=False))

                        #Calculate the standard deviation of list prices versus model projected prices in terms of pct rap (i.e., % difference of model price and listed price from rap list price)
                        total = np.sum(((np.polyval(fit_params, df_plot_range['Weight'])
                                            - df_plot_range['TotalPrice']) 
                                        / (np.polyval(fit_params, df_plot_range['Weight']))) ** 2)

                        curve_shift = math.sqrt(total / len(df_plot_range))

                        #Calculate a residual value - the % difference between predicted price and list price
                        s_residual = (df_plot_range['TotalPrice']-np.polyval(fit_params, df_plot_range['Weight']))/df_plot_range['TotalPrice']
                        df.loc[df_plot_range.index, 'Residual'] = s_residual
                        resid_slope = np.poly1d(np.polyfit(df_plot_range['Weight'],s_residual, 1, full=False))

                        #Store fit parameters in a dictionary
                        if degree == 1:
                            output['Shape'].append(shape_key)
                            output['Color'].append(color)
                            output['Clarity'].append(clar)
                            output['CurveKey'].append(curve_key)
                            output['CurveRangeMin'].append(plot_min)
                            output['CurveRangeMax'].append(plot_max)
                            output['PolyDegree'].append(degree)
                            output['Px2'].append(0)
                            output['Px1'].append(fit_params[1])
                            output['Px0'].append(fit_params[0])
                            output['StdDev'].append(curve_shift)
                            output['NumStones'].append(len(df_plot_range))
                            output['ResidSlope'].append(resid_slope[1]*(fxn_max-fxn_min))
                            output['ResidCept'].append(resid_slope[0])
                        elif degree == 2:
                            output['Shape'].append(shape_key)
                            output['Color'].append(color)
                            output['Clarity'].append(clar)
                            output['CurveKey'].append(curve_key)
                            output['CurveRangeMin'].append(plot_min)
                            output['CurveRangeMax'].append(plot_max)
                            output['PolyDegree'].append(degree)
                            output['Px2'].append(fit_params[2])
                            output['Px1'].append(fit_params[1])
                            output['Px0'].append(fit_params[0])
                            output['StdDev'].append(curve_shift)
                            output['NumStones'].append(len(df_plot_range))
                            output['ResidSlope'].append(resid_slope[1]*(fxn_max-fxn_min))
                            output['ResidCept'].append(resid_slope[0])
                        else:
                            output['Shape'].append(shape_key)
                            output['Color'].append(color)
                            output['Clarity'].append(clar)
                            output['CurveKey'].append(curve_key)
                            output['CurveRangeMin'].append(plot_min)
                            output['CurveRangeMax'].append(plot_max)
                            output['PolyDegree'].append(-999999)
                            output['Px2'].append(-999999)
                            output['Px1'].append(-999999)
                            output['Px0'].append(-999999)
                            output['StdDev'].append(-999999)
                            output['NumStones'].append(len(df_plot_range))
                            output['ResidSlope'].append(-999999)
                            output['ResidCept'].append(-999999)


    #create a dataframe that contains the curve fit parameters
    shape = output['Shape']
    color = output['Color']
    clarity = output['Clarity']
    curvekey = output['CurveKey']
    assert(all([len(shape), len(color), len(clarity), len(curvekey)]))
    columns = ['Shape','Color','Clarity','CurveKey','CurveRangeMin','PolyDegree','Px2','Px1','Px0','StdDev','NumStones', 'ResidSlope', 'ResidCept']
    output2 = { 'Shape' : shape,
                'Color' : color,
                'Clarity' : clarity,
                'CurveKey' : curvekey,
                'CurveRangeMin' : output['CurveRangeMin'],
                'CurveRangeMax' : output['CurveRangeMax'], \
                'PolyDegree' : output['PolyDegree'], \
                'Px2': output['Px2'], \
                'Px1': output['Px1'], \
                'Px0' : output['Px0'], \
                'StdDev': output['StdDev'], \
                'NumStones': output['NumStones'], \
                'ResidSlope': output['ResidSlope'], \
                'ResidCept': output['ResidCept'] \
                }

    df_output = pd.DataFrame(output2,
                     index=['{0}_{1}_{2}_{3}'.format(s,co,cl,cu) 
                                   for s,co,cl,cu in zip(shape, color, clarity, curvekey)
                                  ],
                     columns = ['Shape','Color','Clarity','CurveKey','CurveRangeMin','PolyDegree', 'Px2', 'Px1', 'Px0', 'StdDev', 'NumStones', 'ResidSlope', 'ResidCept'] 
                     )

    df_sel = df_output[((df_output.PolyDegree == 1) & (df_output.Px1 < 0))
                            | ((df_output.PolyDegree == 2) & (df_output.Px1 > 80000))]
    df_output.loc[df_sel.index, 'PolyDegree'] = -999999
    df_output.loc[df_sel.index, 'Px2'] = -999999
    df_output.loc[df_sel.index, 'Px1'] = -999999
    df_output.loc[df_sel.index, 'Px0'] = -999999
    df_output.loc[df_sel.index, 'StdDev'] = -999999
    df_output.loc[df_sel.index, 'ResidSlope'] = -999999
    df_output.loc[df_sel.index, 'ResidCept'] = -999999

    #renaming columns to match database, adding file date

    return df_output

def create_shape_discs(df):
    #create df to be written into excel
    output_df = df[df['Fluorescence Intensity'].isin(fluor_none_and_faint)].groupby(['Shape', 'Color', 'Clarity', 'ShapeDiscKey']).agg({"Price Percentage":np.mean, "Polish":len})
    idx = output_df.index.map(lambda idx: "{}_{}_{}_{}".format(idx[1],idx[2],idx[3],idx[0]))
    output_df = output_df.reset_index()
    output_df.index = idx
    output_df.index.name = 'shapediscountkey'
    output_df.columns = ['shape','color','clarity','minweight','avgdiscount','numstones']
    output_df.loc[:,'rapfiledate'] = pd.Series(utils.file_date_output(), index=output_df.index)
    output_df = output_df[output_df['avgdiscount'].notnull()]

    #write values into DB
    df_upload = output_df.reset_index(level=[0])
    df_upload['numstones'] = df_upload['numstones'].astype(float)

    if os.environ['DB_UPLOAD_TOGGLE'] == "upload-on":
        for i in range(len(df_upload)):
            values = tuple(df_upload.iloc[i])
            cur.execute(utils.shape_discs_upsert_query, values)

    return output_df

def write_excel(df, wp_path, file_date, df_rap_price_list):
    file_name = path.join(wp_path, 'prdt_optimized_{0}.xlsx'.format(datetime.now().strftime("%Y-%m-%d-%H%M")))
    df_price_curves = price_curve_generator_all(df, wp_path, file_date)
    writer = pd.ExcelWriter(file_name)

    #renaming columns to match database, adding file date, and writing to xcel
    df_excel = df_price_curves.copy()
    df_excel.index.name = 'paramkey'
    df_excel.loc[:,'rapfiledate'] = pd.Series(utils.file_date_output(), index=df_excel.index)
    df_excel.rename(columns={'Shape':'shape','Color':'color','Clarity':'clarity','CurveKey':'curvekey','CurveRangeMin':'curverangemin','PolyDegree':'polydegree', 'Px2':'px2', 'Px1':'px1', 'Px0':'px0', 'StdDev':'stddev', 'NumStones':'numstones', 'ResidSlope':'residslope', 'ResidCept':'residcept'}, inplace=True)
    df_excel.to_excel(writer, 'PRICE PARAMS')
    create_shape_discs(df).to_excel(writer, 'SHAPE DISCS')

    # writing price params to DB
    df_excel = df_excel.reset_index(level=[0])
    df_excel['polydegree'] = df_excel['polydegree'].astype(float)
    df_excel['numstones'] = df_excel['numstones'].astype(float)
    if os.environ['DB_UPLOAD_TOGGLE'] == "upload-on":
        for i in range(len(df_excel)):
            if df_excel.iloc[i]['polydegree'] != -999999.0:
                values = tuple(df_excel.iloc[i])
                cur.execute(utils.price_params_upsert_query, values)
            else:
                pass

    df['PriceCurveKey'] = df['Weight'].apply(utils.price_curve_key)
    df_index_cols = ['DiscountShapeKey','Color','Clarity','PriceCurveKey']
    px_curve_index_cols = ['Shape','Color','Clarity','CurveKey']
    px_curve_cols = ['PolyDegree','Px2','Px1','Px0','StdDev']
    df = pd.merge(df, df_price_curves[px_curve_index_cols+px_curve_cols], how="left", 
             left_on  = df_index_cols,
             right_on = px_curve_index_cols,
             suffixes = ['','_c']
            )

    df['PredictedPrice'] = df['Weight']**2 * df['Px2'] + df['Weight'] * df['Px1'] + df['Px0']
    df['PredictedPricePerCarat'] = df['PredictedPrice'] / df['Weight']
    df['PredictedPctRap'] = (df['PredictedPricePerCarat'] - df['RapPricePerCarat']) / df['RapPricePerCarat']
    df['PredictedPercentDiff'] = (df['TotalPrice']-df['PredictedPrice'])/df['PredictedPrice']

    clars = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'SI3', 'I1', 'I2','I3','Blank_Col']
    def get_clars(suffix):
        return [c + suffix for c in clars]

    clars_avg = get_clars("_avg")
    clars_med = get_clars("_med")
    clars_std = get_clars("_std")
    clars_num = get_clars("_num")[:-1]
    clars_blnk = get_clars("")

    clars_tot = clars_avg + clars_med + clars_std + clars_num

    usa_only = ['usa']

    discount_groups = [ [['D'], ['IF', 'VVS1', 'VVS2']], \
                        [['E', 'F'], ['IF', 'VVS1', 'VVS2']], \
                        [['G', 'H', 'I', 'J'], ['IF', 'VVS1', 'VVS2']], \
                        [['D'], ['VS1', 'VS2', 'SI1', 'SI2']], \
                        [['E', 'F'], ['VS1', 'VS2']], \
                        [['G', 'H', 'I', 'J'], ['VS1', 'VS2']], \
                        [['E', 'F'], ['SI1', 'SI2']], \
                        [['G', 'H', 'I', 'J'], ['SI1', 'SI2']], \
                        [['K', 'L'], ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2']]\
                        ]

    ex = ['Excellent']
    vg = ['Very Good']
    gd = ['Good']
    fr = ['Fair']

    vg_plus = ['Excellent', 'Very Good']
    gd_plus = ['Excellent', 'Very Good', 'Good']
    fr_plus = ['Excellent', 'Very Good', 'Good', 'Fair']
    tot = ['Excellent', 'Very Good', 'Good', 'Fair']

    # TAG , CUT , polish, sym, fluor

    discounts = [ \
                ['EX_EX_EX_NO_CPBOOST', ex, ex, ex, fluor_none, usa_only, 'Round', 'RB'], \
                ['EX_EX_EX_NO', ex, ex, ex, fluor_none, all_countries, 'Round', 'RB'], \
                ['EX_EX_EX_FNT', ex, ex, ex, fluor_faint, all_countries, 'Round', 'RB'], \
                ['EX_EX_EX_MED', ex, ex, ex, fluor_medium, all_countries, 'Round', 'RB'], \
                ['EX_EX_EX_STRONG', ex, ex, ex, fluor_strong, all_countries, 'Round', 'RB'], \
                ['VG_VGPLUS_VGPLUS_NO', vg, vg_plus, vg_plus, fluor_none, all_countries, 'Round', 'RB'], \
                ['VG_VGPLUS_VGPLUS_FNT', vg, vg_plus, vg_plus, fluor_faint, all_countries, 'Round', 'RB'], \
                ['VG_VGPLUS_VGPLUS_MED', vg, vg_plus, vg_plus, fluor_medium, all_countries, 'Round', 'RB'], \
                ['VG_VGPLUS_VGPLUS_STRONG', vg, vg_plus, vg_plus, fluor_strong, all_countries, 'Round', 'RB'], \
                ['GD_GDPLUS_GDPLUS_NO', gd, gd_plus, gd_plus, fluor_none, all_countries, 'Round', 'RB'], \
                ['GD_GDPLUS_GDPLUS_FNT', gd, gd_plus, gd_plus, fluor_faint, all_countries, 'Round', 'RB'], \
                ['GD_GDPLUS_GDPLUS_MED', gd, gd_plus, gd_plus, fluor_medium, all_countries, 'Round', 'RB'], \
                ['GD_GDPLUS_GDPLUS_STRONG', gd, gd_plus, gd_plus, fluor_strong, all_countries, 'Round', 'RB'], \
                ['FR_FRPLUS_FRPLUS_NO', fr, fr_plus, fr_plus, fluor_none, all_countries, 'Round', 'RB'], \
                ['FR_FRPLUS_FRPLUS_FNT', fr, fr_plus, fr_plus, fluor_faint, all_countries, 'Round', 'RB'], \
                ['FR_VGPLUS_FRPLUS_MED', fr, fr_plus, fr_plus, fluor_medium, all_countries, 'Round', 'RB'], \
                ['FR_FRPLUS_FRPLUS_STRONG', fr, fr_plus, fr_plus, fluor_strong, all_countries, 'Round', 'RB'], \
                ['ANY_GDPLUS_GD_NO', ["Good", "Very Good"], gd_plus, gd_plus, fluor_none, usa_only, 'Princess', 'PR'], \
                ]

    discount_bins = [ \
                     [0.23, 1.00], \
                     [1.00, 1.50], \
                     [1.50, 2.99], \
                     ]

    df['PredictedPrice'] = df['Weight']**2 * df['Px2'] +  df['Weight'] * df['Px1'] + df['Px0']
    df['PredictedPricePerCarat'] = df['PredictedPrice'] / df['Weight']
    df['PredictedPctRap'] = (df['PredictedPricePerCarat'] - df['RapPricePerCarat']) / df['RapPricePerCarat']

    discount_output = { 'Tag' : [], 'RB Avg Discount': [], 'RB Median Discount' : [], 'RB Discount Stdev' : [], 'Num Stones' : [], \
                             'PR DepthDiff Coefficient' : [], 'PR Sym Rank Coefficient' : [], \
                             'PR DepthDiff T-Stat' : [], 'PR Sym Rank T-Stat' : []}

    for p in range(len(discount_bins)):
        min_carat = discount_bins[p][0]
        max_carat = discount_bins[p][1]
        df_bin = df[(df.Weight >= min_carat) & (df.Weight < max_carat) & (df.Px2 != -999999)]
        for i in range(len(discounts)):
            df_avg_discount = pd.DataFrame(0, index=colors, columns=clars_blnk, dtype=np.float64)
            df_med_discount = pd.DataFrame(0, index=colors, columns=clars_blnk, dtype=np.float64)
            df_std_discount = pd.DataFrame(0, index=colors, columns=clars_blnk, dtype=np.float64)
            df_number_of_stones = pd.DataFrame(0, index=colors, columns=clars, dtype=np.float64)

            tag = discounts[i][0]
            cut = discounts[i][1]
            polish = discounts[i][2]
            sym = discounts[i][3]
            fluor = discounts[i][4]
            location = discounts[i][5]
            shape = discounts[i][6]
            shape_tag = discounts[i][7]

            df_discount = df_bin[ \
                (df_bin['Shape'] == shape)
                & (df_bin['Supplier country'].str.lower().isin(location)) \
                & (df_bin['Cut'].isin(cut)) \
                & (df_bin['Polish'].isin(polish)) \
                & (df_bin['Symmetry'].isin(sym)) \
                & (df_bin['Fluorescence Intensity'].isin(fluor)) \
                ] #

            for m in range(len(discount_groups)):
                color = discount_groups[m][0]
                clar = discount_groups[m][1]

                df_temp = df_discount[(df_discount['Color'].isin(color)) & (df_discount['Clarity'].isin(clar))]


                avg_discount = np.mean(df_temp['ExactPctRap'] - df_temp['PredictedPctRap'])
                med_discount = np.median(df_temp['ExactPctRap'] - df_temp['PredictedPctRap'])
                std_discount = np.std(df_temp['ExactPctRap'] - df_temp['PredictedPctRap'])
                if math.isnan(avg_discount):
                    avg_discount = -999999
                    med_discount = -999999
                    std_discount = -999999

                if shape == 'Round':
                    if len(df_temp) == 0:
                        for j in discount_groups[m][0]:
                            for k in discount_groups[m][1]:
                                df_number_of_stones.loc[j,k] = 0
                                df_avg_discount.loc[j,k] = -999999
                                df_med_discount.loc[j,k] = -999999
                                df_std_discount.loc[j,k] = -999999
                                discount_output['Tag'].append("%s_%sct_%sct_%s_%s_%s" %(shape_tag,min_carat,max_carat,j,k,tag))
                                discount_output['RB Avg Discount'].append(-999999)
                                discount_output['RB Median Discount'].append(-999999)
                                discount_output['RB Discount Stdev'].append(-999999)
                                discount_output['Num Stones'].append(0)
                                discount_output['PR DepthDiff Coefficient'].append(-999999)
                                discount_output['PR Sym Rank Coefficient'].append(-999999)
                                discount_output['PR DepthDiff T-Stat'].append(-999999)
                                discount_output['PR Sym Rank T-Stat'].append(-999999)

                    elif len(df_temp) <= 7:
                        for j in discount_groups[m][0]:
                            for k in discount_groups[m][1]:
                                df_number_of_stones.loc[j,k] = len(df_temp)
                                df_avg_discount.loc[j,k] = -999999
                                df_med_discount.loc[j,k] = -999999
                                df_std_discount.loc[j,k] = -999999
                                discount_output['Tag'].append("%s_%sct_%sct_%s_%s_%s" %(shape_tag,min_carat,max_carat,j,k,tag))
                                discount_output['RB Avg Discount'].append(-999999)
                                discount_output['RB Median Discount'].append(-999999)
                                discount_output['RB Discount Stdev'].append(-999999)
                                discount_output['Num Stones'].append(len(df_temp))
                                discount_output['PR DepthDiff Coefficient'].append(-999999)
                                discount_output['PR Sym Rank Coefficient'].append(-999999)
                                discount_output['PR DepthDiff T-Stat'].append(-999999)
                                discount_output['PR Sym Rank T-Stat'].append(-999999)

                    else:
                        for j in discount_groups[m][0]:
                            for k in discount_groups[m][1]:
                                df_number_of_stones.loc[j,k] = len(df_temp)
                                df_avg_discount.loc[j,k] = avg_discount
                                df_med_discount.loc[j,k] = med_discount
                                df_std_discount.loc[j,k] = std_discount
                                discount_output['Tag'].append("%s_%sct_%sct_%s_%s_%s" %(shape_tag,min_carat,max_carat,j,k,tag))
                                discount_output['RB Avg Discount'].append(avg_discount)
                                discount_output['RB Median Discount'].append(med_discount)
                                discount_output['RB Discount Stdev'].append(std_discount)
                                discount_output['Num Stones'].append(len(df_temp))
                                discount_output['PR DepthDiff Coefficient'].append(-999999)
                                discount_output['PR Sym Rank Coefficient'].append(-999999)
                                discount_output['PR DepthDiff T-Stat'].append(-999999)
                                discount_output['PR Sym Rank T-Stat'].append(-999999)

                elif shape == 'Princess':
                    if len(df_temp) == 0:
                        for j in discount_groups[m][0]:
                            for k in discount_groups[m][1]:
                                df_number_of_stones.loc[j,k] = 0
                                discount_output['Tag'].append("%s_%sct_%sct_%s_%s_%s" %(shape_tag,min_carat,max_carat,j,k,tag))
                                discount_output['RB Avg Discount'].append(-999999)
                                discount_output['RB Median Discount'].append(-999999)
                                discount_output['RB Discount Stdev'].append(-999999)
                                discount_output['PR DepthDiff Coefficient'].append(-999999)
                                discount_output['PR Sym Rank Coefficient'].append(-999999)
                                discount_output['Num Stones'].append(0)
                                discount_output['PR DepthDiff T-Stat'].append(-999999)
                                discount_output['PR Sym Rank T-Stat'].append(-999999)

                    elif len(df_temp) <= 12:
                        for j in discount_groups[m][0]:
                            for k in discount_groups[m][1]:
                                df_number_of_stones.loc[j,k] = len(df_temp)
                                discount_output['Tag'].append("%s_%sct_%sct_%s_%s_%s" %(shape_tag,min_carat,max_carat,j,k,tag))
                                discount_output['RB Avg Discount'].append(-999999)
                                discount_output['RB Median Discount'].append(-999999)
                                discount_output['RB Discount Stdev'].append(-999999)
                                discount_output['PR DepthDiff Coefficient'].append(-999999)
                                discount_output['PR Sym Rank Coefficient'].append(-999999)
                                discount_output['Num Stones'].append(len(df_temp))
                                discount_output['PR DepthDiff T-Stat'].append(-999999)
                                discount_output['PR Sym Rank T-Stat'].append(-999999)

                    else:
                        try: 
                            df_regress_temp = df_temp[(df_temp['PredictedPercentDiff'] <= 0.1) & (df_temp['Weight'] >= .4)]
                            df_princess_regression = pd.DataFrame([df_regress_temp['PredictedPercentDiff'],df_regress_temp['DepthDiff'],df_regress_temp['SymRank']]).transpose()

                            y = df_princess_regression['PredictedPercentDiff']
                            X = sm.add_constant(df_princess_regression.drop(['PredictedPercentDiff'], axis = 1))
                            model = sm.OLS(y, X)
                            reg_results = model.fit()

                            for j in discount_groups[m][0]:
                                for k in discount_groups[m][1]:
                                    df_number_of_stones.loc[j,k] = len(df_temp)
                                    discount_output['Tag'].append("%s_%sct_%sct_%s_%s_%s" %(shape_tag,min_carat,max_carat,j,k,tag))
                                    discount_output['RB Avg Discount'].append(-999999)
                                    discount_output['RB Median Discount'].append(-999999)
                                    discount_output['RB Discount Stdev'].append(-999999)
                                    discount_output['PR DepthDiff Coefficient'].append(reg_results.params[0])
                                    discount_output['PR Sym Rank Coefficient'].append(reg_results.params[1])
                                    discount_output['Num Stones'].append(len(df_temp))
                                    discount_output['PR DepthDiff T-Stat'].append(reg_results.tvalues[0])
                                    discount_output['PR Sym Rank T-Stat'].append(reg_results.tvalues[1])
                        except:
                            for j in discount_groups[m][0]:
                                for k in discount_groups[m][1]:
                                    df_number_of_stones.loc[j,k] = len(df_temp)
                                    discount_output['Tag'].append("%s_%sct_%sct_%s_%s_%s" %(shape_tag,min_carat,max_carat,j,k,tag))
                                    discount_output['RB Avg Discount'].append(-999999)
                                    discount_output['RB Median Discount'].append(-999999)
                                    discount_output['RB Discount Stdev'].append(-999999)
                                    discount_output['PR DepthDiff Coefficient'].append(-999999) # 'params' are betas for OLS
                                    discount_output['PR Sym Rank Coefficient'].append(-999999)
                                    discount_output['Num Stones'].append(len(df_temp))
                                    discount_output['PR DepthDiff T-Stat'].append(-999999)
                                    discount_output['PR Sym Rank T-Stat'].append(-999999)

    arrays = [discount_output['Tag']]
    tuples = zip(*arrays)
    index = pd.MultiIndex.from_tuples(tuples)

    df_discount_output = pd.DataFrame(discount_output, index=index,  columns=['RB Avg Discount', 'RB Median Discount', 'RB Discount Stdev', 'PR DepthDiff Coefficient', 'PR Sym Rank Coefficient', 'PR DepthDiff T-Stat', 'PR Sym Rank T-Stat', 'Num Stones'])
 
    #rename columns and add file date before passing to excel
    df_discount_output.loc[:,'rapfiledate'] = pd.Series(utils.file_date_output(), index=df_discount_output.index)
    new_cols=['rbavgdiscount', 'rbmediandiscount', 'rbdiscountstdev', 'prdepthdiffcoefficient', 'prsymrankcoefficient', 'prdepthdifftstat', 'prsymranktstat', 'numstones', 'rapfiledate']
    df_discount_output.rename(columns=dict(zip(df_discount_output.columns, new_cols)),inplace=True)
    df_discount_output.to_excel(writer, 'DISCOUNTS LIST')

    #create new temporary DF to upload to postgres
    df_out = df_discount_output.reset_index(level=[0])
    df_out['prdepthdiffcoefficient'] = df_out['prdepthdiffcoefficient'].astype(float)
    df_out['prsymrankcoefficient'] = df_out['prsymrankcoefficient'].astype(float)
    df_out['prdepthdifftstat'] = df_out['prdepthdifftstat'].astype(float)
    df_out['prsymranktstat'] = df_out['prsymranktstat'].astype(float)
    df_out['numstones'] = df_out['numstones'].astype(float)

    if os.environ['DB_UPLOAD_TOGGLE'] == "upload-on":
        for i in range(len(df_out)):
            if (df_out.iloc[i]['rbavgdiscount'] != -999999.0 and df_out.iloc[i]['level_0'].startswith("RB_")) or \
            df_out.iloc[i]['prsymrankcoefficient'] != -999999.0 and df_out.iloc[i]['level_0'].startswith("PR_"):
                values = tuple(df_out.iloc[i])
                cur.execute(utils.discount_upsert_query, values)
            else:
                pass

    #load rap price list, rename columns, reformat date, write to excel
    temp = df_rap_price_list #.reset_index()
    temp.columns = ['Shape','Clarity','Color','Min Wght','Max Wght','Price','Date']
    temp['pricelistkey'] = temp.apply(lambda x: '%s_%s_%s_%s' %(x['Shape'], x['Color'], x['Clarity'], x['Min Wght']), axis=1)
    temp = temp.set_index(['pricelistkey'])
    new_cols = ['shape','clarity','color','minweight','maxweight','price','lastpricechangedate']
    temp.rename(columns=dict(zip(temp.columns, new_cols)),inplace=True)
    temp.to_excel(writer, 'RAP PRICE LIST')

    #upload rap price list to DB
    temp = temp.reset_index(level=[0])
    temp['price'] = temp['price'].astype(float)
    if os.environ['DB_UPLOAD_TOGGLE'] == "upload-on" and datetime.today().weekday() == 5: #only attempt once per week
        for i in range(len(temp)):
            values = temp.iloc[i]
            cur.execute(utils.rap_price_list_upsert_query, values)

    pd.DataFrame({'Date': [file_date]}).to_excel(writer, 'sheet1')
    writer.save()
    utils.upload_to_gcloud("curvecalcoutput", file_name, file_name.split("_")[-1])

def load_data(file_date):
    d = datetime.strptime(file_date, "%Y%m%d")

    # Load latest rapnet data dump
    # rap_data_file = '/local/2019-01-31-FullRapFile.csv'
    # rap_data_file = '/local/rap-test-data.csv'
    rap_data_file = utils.get_gcloud_file("rapdvtfiles", todays_filename) 
    current_df = pd.read_csv(rap_data_file, dtype=csv_data_types, usecols=csv_columns)

    #import rappaport price list
    # price_list_file = '/local/rap-price-list.csv'
    price_list_file = utils.get_gcloud_file("rappricelists", utils.last_fridays_date() + "-RapPriceList.csv")
    df_rap_price_list =  pd.read_csv(price_list_file, sep=',', header=0,\
        names = ['Shape','Clarity','Color','MinCarat','MaxCarat','PricePerCar','Date'])     

    # filter out bad rows here - update in future if necessary
    current_df['RapPriceKey'] = current_df['Weight'].apply(utils.rap_price_key)
    current_df['RapShapeKey'] = current_df['Shape'].apply(utils.rap_shape_key)
    current_df = current_df[(current_df.Lab == "GIA") & (current_df['Price Per Carat'] > 0)] 

    df = pd.merge(current_df, df_rap_price_list, how = 'left', left_on = ['RapShapeKey','Color','Clarity','RapPriceKey'],
                   right_on = ['Shape','Color','Clarity','MinCarat'], suffixes = ['','_pl'])

    df.rename(columns={'PricePerCar':'RapPricePerCarat'}, inplace=True)

    df['TotalPrice'] = df['Price Per Carat'] * df['Weight'] #l.Price represents price per carat
    df['ShapeDiscKey'] = df['Weight'].apply(utils.shape_disc_key)
    df['DiscountShapeKey'] = df['Shape'].apply(utils.discount_shape_key)
    df.loc[df[df.RapPricePerCarat.isnull()].index, 'RapPricePerCarat'] = -999999
    df['ExactPctRap'] = (df['Price Per Carat'] - df['RapPricePerCarat']) / df['RapPricePerCarat']
    df['Ratio'] = df['Measurements'].apply(utils.ratio)
    df['DepthDiff'] = df['Depth Percent'].apply(utils.depth_diff)
    df['RatioDiff'] = df['Ratio'].apply(utils.ratio_diff)
    df['SymRank'] = df['Symmetry'].apply(utils.grade_rank)

    df_p = df.query('Shape == "Princess"')

    utils.grade_princess_cuts(df, df_p, 56.0, 82.0, 1.25, ['Excellent','Very Good','Good'], ['Excellent','Very Good','Good','Fair'], 'Good')
    utils.grade_princess_cuts(df, df_p, 62.0, 75.0, 1.10, ['Excellent','Very Good', 'Good','Fair'], ['Excellent','Very Good','Good','Fair'], 'Very Good')
    utils.grade_princess_cuts(df, df_p, 64.0, 72.0, 1.05, ['Excellent','Very Good', 'Good'], ['Excellent','Very Good','Good'], 'Excellent')

    return (df, df_rap_price_list)

def run(file_date):
    df, df_rap_price_list = load_data(file_date)
    write_excel(df, wp_path, file_date, df_rap_price_list)


try:
    conn = psycopg2.connect(host=os.environ['DB_HOST'], port='5432', sslmode='disable', dbname=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PW'])
    cur = conn.cursor()
    start_time = datetime.now()
    todays_filename = datetime.today().strftime("%Y-%m-%d")+'-FullRapFile.csv'
    if __name__ == '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('--date', help='date to process')
        args = parser.parse_args()
        file_date = datetime.now().strftime("%Y%m%d")
        if args.date:
            file_date = args.date
        run(file_date)
    conn.commit()
    conn.close()

    end_time=datetime.now()
    duration = end_time - start_time
    message =  """\
    Subject: Curvecalc.py Successful

    Start Time = {0} \n
    End Time = {1} \n
    Run Duration = {2} \n
    Filename =  {3} \n
    Hostname = {4} \n
    \n
    HUZZAH!!""".format(start_time, end_time, duration, todays_filename, os.environ['VM_NAME'])
    if os.environ['SUCCESS_EMAIL_TOGGLE'] == 'EmailOn':
        utils.send_email("joe.mellet@gmail.com", message)
    if os.environ['VM_NAME'] != 'JHMLaptop':
        utils.stop_server(os.environ['VM_NAME'])

except Exception as e:
    message =  """\
    Subject: Curvecalculator Failed

    Error = {0} \n
    \n
    """.format(e)
    if os.environ['FAIL_EMAIL_TOGGLE'] == 'EmailOn':
        utils.send_email("joe.mellet@gmail.com", message)
    if os.environ['VM_NAME'] != 'JHMLaptop':
        utils.stop_server(os.environ['VM_NAME'])
