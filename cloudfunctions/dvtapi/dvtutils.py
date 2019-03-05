



clarity_ranks = {"IF":1, "VVS1":2, "VVS2":3, "VS1":4, "VS2":5, "SI1":5, "SI2":7, "I1":8, "I2":9}
color_ranks = {"D":1, "E":2, "F":3, "G":4, "H":5, "I":6, "J":7, "K":8, "L":9, "M":10, "N":11}


valid_values = {
"api_key" : {"type":(str)}, 
"request_type" : {"type":(str)}, 
"user" : {"type":(str), "type_err_msg":"invalid value for user - expected string"} ,
"shape" : {"type":(str), "type_err_msg":"invalid value for shape - expected string", "allow_vals":["round","princess"]},
"weight" : {"type":(float), "type_err_msg":"invalid value for weight - expected float"},
"color" : {"type":(str), "type_err_msg":"invalid value for shape - expected string", "allow_vals":['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']},
"clarity" : {"type":(str), "type_err_msg":"invalid value for shape - expected string", "allow_vals":['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'SI3', 'I1', 'I2', 'I3']},
"cert_lab" : {"type":(str), "type_err_msg":"invalid value for lab - expected string", "allow_vals":["gia","x"]},
"recut" : {"type":"bool", "type_warn_msg":"no value for recut detected", "allow_vals":[True, False]},
"cut_grade": "STONE CUT GRADE - STRING - REQUIRED FOR ROUNDS", 
"polish" : "STONE POLISH GRADE GRADE STRING - REQUIRED FOR ROUNDS", 
"symmetry" : "STONE SYMMETRY GRADE GRADE STRING - REQUIRED FOR ROUNDS", 
"fluor" : "STONE FLUORESENCE - STRING - REUIRED - ALLOWABLE VALS = ",
"depth_percent":"",
"table_percent":"",
"side_len_1":"",
"side_len_2":"",
"metal_type":"",
"metal_weight":"",
"laser_drilled":"",
"fracture_filled":"",
"color_enhanced":"",
"synthetic_diamond":"",
"hthp":"",
"tint":"",
"milkiness":"",
"centre_pique":"",
"black_pique":""
}

# to do ... check floats and booleans for valid values
def check_values(json, errs, warns):
    req_values = ["api_key", "shape", "weight", "color", "clarity"]
    if all(elem in json.keys() for elem in req_values):
        pass
    else:
        errs.append("JSON body is missing required values. The following keys are required in the JSON body: {}".format(req_values))
    for key in json.keys():
        print(key)
        if key in valid_values.keys():
            if isinstance(json[key], valid_values[key]['type']):
                if 'allow_vals' in valid_values[key].keys() and json[key] not in valid_values[key]['allow_vals']:
                    errs.append("Invalid values for {0} - Received \'{1}\', expected one of the following: {2}. ".format(key, json[key], valid_values[key]['allow_vals']))
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




