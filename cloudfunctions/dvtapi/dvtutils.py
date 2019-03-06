



clarity_ranks = {"IF":1, "VVS1":2, "VVS2":3, "VS1":4, "VS2":5, "SI1":5, "SI2":7, "I1":8, "I2":9}
color_ranks = {"D":1, "E":2, "F":3, "G":4, "H":5, "I":6, "J":7, "K":8, "L":9, "M":10, "N":11}


valid_values = {
"api_key" : {"type":(str), "max_len":50}, 
"request_type" : {"type":(str),"allow_vals":["estimate","price","all"]}, 
"user" : {"type":(str), "max_len":50},
"shape" : {"type":(str), "allow_vals":["Round", "Princess", "Cushion Modified", "Emerald", "Pear", "Marquise", "Radiant", "Oval", "Heart", "Asscher"]},
"weight" : {"type":(float), "min":0, "max":100},
"color" : {"type":(str), "allow_vals":['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']},
"clarity" : {"type":(str), "allow_vals":['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'SI3', 'I1', 'I2', 'I3']},
"cert_lab" : {"type":(str), "allow_vals":["GIA",""]},
"recut" : {"type":(str), "allow_vals":["Yes", "No"]},
"cut_grade": {"type":(str), "allow_vals":['EX', 'VG', 'G', 'F', 'P']},
"polish" : {"type":(str), "allow_vals":['EX', 'VG', 'G', 'F', 'P']}, 
"symmetry" : {"type":(str), "allow_vals":['EX', 'VG', 'G', 'F', 'P']}, 
"fluor" : {"type":(str), "allow_vals":['None', 'Faint', 'Medium', 'Strong', 'Very Strong']},
"depth_percent": {"type":(float), "min":10, "max":100},
"table_percent": {"type":(float), "min":10, "max":100},
"side_len_1": {"type":(float), "min":0.1, "max":100},
"side_len_2": {"type":(float), "min":0.1, "max":100},
"metal_type": {"type":(str), "allow_vals":["9 Kt Gold","10 Kt Gold","14 Kt Gold","16 Kt Gold","18 Kt Gold","22 Kt Gold","24 Kt Gold","Platinum","Silver","None"]},
"metal_weight": {"type":(float), "min":0, "max":100},
"laser_drilled": {"type":(str), "allow_vals":["None","1 Small","1 Large","Multiple"]},
"fracture_filled": {"type":(str), "allow_vals":["None","Well Done","Reasonable","Weak"]},
"color_enhanced": {"type":(str), "allow_vals":["None", "Blue", "Yellow", "Black", "Brown"]},
"synthetic_diamond": {"type":(str), "allow_vals":["Yes", "No"]},
"hthp": {"type":(str), "allow_vals":["Yes", "No"]},
"tint": {"type":(str), "allow_vals":["None", "Yellow", "Brown", "Green", "Grey"]},
"milkiness": {"type":(str), "allow_vals":["None", "Light", "Medium", "Strong"]},
"centre_pique": {"type":(str), "allow_vals":["Yes", "No"]},
"black_pique": {"type":(str), "allow_vals":["Yes", "No"]},
}
req_values = ["api_key", "shape", "weight", "color", "clarity"]


# to do ... check floats and booleans for valid values
def check_json_values(json, errs):
    req_values = ["api_key", "shape", "weight", "color", "clarity"]
    # check json contains all required keys
    if all(elem in json.keys() for elem in req_values):
        pass
    else:
        errs.append("JSON body is missing required values. The following keys are required in the JSON body: {}".format(req_values))
        print(json[key])
    for key in json.keys():
        if key in valid_values.keys():
            # check datatype of json against expected
            if isinstance(json[key], valid_values[key]['type']):
                # check json strings against expected values 
                if 'allow_vals' in valid_values[key].keys() and json[key] not in valid_values[key]['allow_vals']:
                    errs.append("Invalid values for {0} - Received \'{1}\', expected one of the following: {2}. ".format(key, json[key], valid_values[key]['allow_vals']))
                elif 'max_len' in valid_values[key].keys() and valid_values[key]['max_len'] < len(json[key]):
                    errs.append("Invalid string length for {0} - Received string \'{1}\', char limit is {2}. ".format(key, json[key], valid_values[key]['max_len']))
                elif 'min' in valid_values[key].keys() and (valid_values[key]['min'] > json[key] or valid_values[key]['max'] < json[key]):
                    errs.append("Invalid value for {0}. Received {1}, allowed min is {2} and allowed max is {3}".format(key, json[key], valid_values[key]['min'], valid_values[key]['max']))
            else:
                errs.append("Invalid datatype for {0} - Expected {1}, received {2}. ".format(key, valid_values[key]['type'], type(json[key])))



def get_curve_key(weight):
    if weight >= 0.01 and weight <= 0.03:
        return 'r01'
    elif weight >= 0.04 and weight <= 0.07:
        return 'r04'
    elif weight >= 0.08 and weight <= 0.14:
        return 'r08'
    elif weight >= 0.15 and weight <= 0.17:
        return 'r15'
    elif weight >= 0.18 and weight <= 0.22:
        return 'r18'
    elif weight >= 0.23 and weight <= 0.29:
        return 'r23'
    elif weight >= 0.30 and weight <= 0.39:
        return 'r30'
    elif weight >= 0.40 and weight <= 0.49:
        return 'r40'
    elif weight >= 0.50 and weight <= 0.59:
        return 'r50'
    elif 0.60 <= weight and weight <= 0.69:
        return 'r60'
    elif 0.70 <= weight and weight <= 0.79:
        return 'r70'
    elif 0.80 <= weight and weight <= 0.89:
        return 'r80'
    elif 0.90 <= weight and weight <= 0.99:
        return 'r90'
    elif 1.00 <= weight and weight <= 1.49:
        return 'rc1'
    elif 1.50 <= weight and weight <= 1.99:
        return 'rcr'
    elif 2.00 <= weight and weight <= 2.99:
        return 'rc2'
    elif 3.00 <= weight and weight <= 3.99:
        return 'rc3'
    elif 4.00 <= weight and weight <= 4.99:
        return 'rc4'
    elif 5.00 <= weight and weight <= 9.99:
        return 'rc5'
    else:
        return 'rct'

def get_price_params(json):
    clar = json['clarity']
    color = json['color']
    shape_key = ""
    weight_key = get_curve_key(json['weight'])
    if json['shape'].lower() == "round":
        shape_key = "RB"
    else:
        shape_key = "PR"
    return "{0}_{1}_{2}_{3}".format(shape_key, color, clar, weight_key)


def check_api_key(request_json, error_list):
    try:
        if request_json['api_key'] != "secretsarenofun":
            error_list.append("ERROR: Incorrect api_key!")
    except KeyError:
        error_list.append("ERROR: api_key not found in body of request!")


