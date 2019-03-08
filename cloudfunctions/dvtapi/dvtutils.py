


clarity_ranks = {'IF':1, 'VVS1':2, 'VVS2':3, 'VS1':4, 'VS2':5, 'SI1':5, 'SI2':7, 'I1':8, 'I2':9}
color_ranks = {'D':1, 'E':2, 'F':3, 'G':4, 'H':5, 'I':6, 'J':7, 'K':8, 'L':9, 'M':10, 'N':11}


valid_values = {
'api_key' : {'type':(str), 'max_len':50}, 
'request_type' : {'type':(str),'allow_vals':['estimate','price','all']}, 
'user' : {'type':(str), 'max_len':50},
'shape' : {'type':(str), 'allow_vals':['Round', 'Pear', 'Cushion Modified', 'Princess', 'Emerald', 'Oval', 'Radiant', 'Marquise', 'Heart', 'Asscher', 'Cushion Brilliant', 'Sq. Emerald']},
'weight' : {'type':(float), 'min':0, 'max':100},
'color' : {'type':(str), 'allow_vals':['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']},
'clarity' : {'type':(str), 'allow_vals':['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'SI3', 'I1', 'I2', 'I3']},
'cert_lab' : {'type':(str), 'allow_vals':['GIA','']},
'recut' : {'type':(str), 'allow_vals':['Yes', 'No']},
'cut_grade': {'type':(str), 'allow_vals':['EX', 'VG', 'G', 'F', 'P']},
'polish' : {'type':(str), 'allow_vals':['EX', 'VG', 'G', 'F', 'P']}, 
'symmetry' : {'type':(str), 'allow_vals':['EX', 'VG', 'G', 'F', 'P']}, 
'fluor' : {'type':(str), 'allow_vals':['None', 'Faint', 'Medium', 'Strong', 'Very Strong']},
'depth_percent': {'type':(float), 'min':10, 'max':100},
'table_percent': {'type':(float), 'min':10, 'max':100},
'side_len_1': {'type':(float), 'min':0.1, 'max':100},
'side_len_2': {'type':(float), 'min':0.1, 'max':100},
'metal_type': {'type':(str), 'allow_vals':['9 Kt Gold','10 Kt Gold','14 Kt Gold','16 Kt Gold','18 Kt Gold','22 Kt Gold','24 Kt Gold','Platinum','Silver','None']},
'metal_weight': {'type':(float), 'min':0, 'max':100},
'laser_drilled': {'type':(str), 'allow_vals':['None','1 Small','1 Large','Multiple']},
'fracture_filled': {'type':(str), 'allow_vals':['None','Well Done','Reasonable','Weak']},
'color_enhanced': {'type':(str), 'allow_vals':['None', 'Blue', 'Yellow', 'Black', 'Brown']},
'synthetic_diamond': {'type':(str), 'allow_vals':['Yes', 'No']},
'hthp': {'type':(str), 'allow_vals':['Yes', 'No']},
'tint': {'type':(str), 'allow_vals':['None', 'Yellow', 'Brown', 'Green', 'Grey']},
'milkiness': {'type':(str), 'allow_vals':['None', 'Light', 'Medium', 'Strong']},
'centre_pique': {'type':(str), 'allow_vals':['Yes', 'No']},
'black_pique': {'type':(str), 'allow_vals':['Yes', 'No']},
}
req_values = ['api_key', 'shape', 'weight', 'color', 'clarity', 'fluor']

# to do ... check floats and booleans for valid values
def check_json_values(json, errs):
    # check json contains all required keys
    if all(elem in json.keys() for elem in req_values):
        pass
    else:
        errs.append('JSON body is missing required values. The following keys are required in the JSON body: {}'.format(req_values))
        print(json[key])
    for key in json.keys():
        if key in valid_values.keys():
            # check datatype of json against expected
            if isinstance(json[key], valid_values[key]['type']):
                # check json strings against expected values 
                if 'allow_vals' in valid_values[key].keys() and json[key] not in valid_values[key]['allow_vals']:
                    errs.append('Invalid values for {0} - Received \'{1}\', expected one of the following: {2}. '.format(key, json[key], valid_values[key]['allow_vals']))
                elif 'max_len' in valid_values[key].keys() and valid_values[key]['max_len'] < len(json[key]):
                    errs.append('Invalid string length for {0} - Received string \'{1}\', char limit is {2}. '.format(key, json[key], valid_values[key]['max_len']))
                elif 'min' in valid_values[key].keys() and (valid_values[key]['min'] > json[key] or valid_values[key]['max'] < json[key]):
                    errs.append('Invalid value for {0}. Received {1}, allowed min is {2} and allowed max is {3}'.format(key, json[key], valid_values[key]['min'], valid_values[key]['max']))
            else:
                errs.append('Invalid datatype for {0} - Expected {1}, received {2}. '.format(key, valid_values[key]['type'], type(json[key])))

def get_curve_key(json):
    weight = json['weight']
    if weight >= 0.01 and weight < 0.04:
        return 'r01', '0.01', 'no_result', '0.01'
    elif weight >= 0.04 and weight < 0.08:
        return 'r04', '0.04', 'no_result', '0.04'
    elif weight >= 0.08 and weight < 0.15:
        return 'r08', '0.08', 'no_result', '0.08'
    elif weight >= 0.15 and weight < 0.18:
        return 'r15', '0.15', 'no_result', '0.15'
    elif weight >= 0.18 and weight < 0.23:
        return 'r18', '0.18', 'no_result', '0.18'
    elif weight >= 0.23 and weight < 0.3:
        return 'r23', '0.23', '0.23ct_1.0ct', '0.23'
    elif weight >= 0.30 and weight < 0.4:
        return 'r30', '0.3', '0.23ct_1.0ct', '0.3'
    elif weight >= 0.40 and weight < 0.5:
        return 'r40', '0.4', '0.23ct_1.0ct', '0.4'
    elif weight >= 0.50 and weight < 0.6:
        return 'r50', '0.5', '0.23ct_1.0ct', '0.5'
    elif 0.60 <= weight and weight < 0.7:
        return 'r60', '0.6', '0.23ct_1.0ct', '0.5'
    elif 0.70 <= weight and weight < 0.8:
        return 'r70', '0.7', '0.23ct_1.0ct', '0.7'
    elif 0.80 <= weight and weight < 0.9:
        return 'r80', '0.8', '0.23ct_1.0ct', '0.7'
    elif 0.90 <= weight and weight < 1.0:
        return 'r90', '0.9', '0.23ct_1.0ct', '0.9'
    elif 1.00 <= weight and weight < 1.25:
        return 'rc1', '1.0', '1.0ct_1.5ct', '1.0'
    elif 1.25 <= weight and weight < 1.5:
        return 'rc1', '1.25', '1.0ct_1.5ct', '1.0'
    elif 1.50 <= weight and weight < 1.75:
        return 'rcr', '1.5', '1.5ct_2.99ct', '1.5'
    elif 1.75 <= weight and weight < 2.0:
        return 'rcr', '1.75', '1.5ct_2.99ct', '1.5'
    elif 2.00 <= weight and weight < 2.5:
        return 'rc2', '2.0', '1.5ct_2.99ct', '2.0'
    elif 2.50 <= weight and weight < 3.0:
        return 'rc2', '2.5', '1.5ct_2.99ct', '2.0'
    elif 3.00 <= weight and weight < 4.0:
        return 'rc3', '3.0', 'no_result', '3.0'
    elif 4.00 <= weight and weight < 5.0:
        return 'rc4', '4.0', 'no_result', '4.0'
    elif 5.00 <= weight and weight < 10.0:
        return 'rc5', '5.0', 'no_result', '5.0'
    else:
        return 'rct', '10.0', 'no_result', '10.0'

def get_shape_key(json):
    if json['shape'] == 'Round':
        return 'RB', 'BR'
    else:
        return 'PR', 'PS'

def get_discount_group_key(json):
    if json['shape'] != 'Round' or json['shape'] != 'Princess':
        return 'no_result'
    elif json['Shape'] == 'Princess':
        return 'ANY_GDPLUS_GD_NO'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'EX' and json['fluor'] == 'None':
        return 'EX_EX_EX_NO'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'EX' and json['fluor'] == 'Faint':
        return 'EX_EX_EX_FNT'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'EX' and json['fluor'] == 'Medium':
        return 'EX_EX_EX_MED'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'EX' and json['fluor'] == 'Strong':
        return 'EX_EX_EX_STRONG'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'VG' and json['fluor'] == 'None':
        return 'VG_VGPLUS_VGPLUS_NO'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'VG' and json['fluor'] == 'Faint':
        return 'VG_VGPLUS_VGPLUS_FNT'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'VG' and json['fluor'] == 'Medium':
        return 'VG_VGPLUS_VGPLUS_MED'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'VG' and json['fluor'] == 'Strong':
        return 'VG_VGPLUS_VGPLUS_STRONG'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'G' and json['fluor'] == 'None':
        return 'GD_GDPLUS_GDPLUS_NO'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'G' and json['fluor'] == 'Faint':
        return 'GD_GDPLUS_GDPLUS_FNT'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'G' and json['fluor'] == 'Medium':
        return 'GD_GDPLUS_GDPLUS_MED'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'G' and json['fluor'] == 'Strong':
        return 'GD_GDPLUS_GDPLUS_STRONG'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'F' and json['fluor'] == 'None':
        return 'FR_FRPLUS_FRPLUS_NO'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'F' and json['fluor'] == 'Faint':
        return 'FR_FRPLUS_FRPLUS_FNT'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'F' and json['fluor'] == 'Medium':
        return 'FR_FRPLUS_FRPLUS_MED'
    elif json['shape'] == 'Round' and json['cut_grade'] == 'F' and json['fluor'] == 'Strong':
        return 'FR_FRPLUS_FRPLUS_STRONG'
    else:
        return 'no_result'

def check_api_key(json, error_list):
    try:
        if json['api_key'] != 'secretsarenofun':
            error_list.append('ERROR: Incorrect api_key!')
    except KeyError:
        error_list.append('ERROR: api_key not found in body of request!')


