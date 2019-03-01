import flask as f
import logging



# Google sample code - https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/functions/helloworld/main.py
# HTTP Request documentation - https://cloud.google.com/functions/docs/writing/http

### PROOF OF CONCEPT:
# Receive POST request from Salesfroce
def dvt_api(request):
	request_json = request.get_json(silent=True)
	errs = []
	succ = []
	def check_api_key(request_json, success_list, error_list):
		if not request_json['api_key']:
			error_list.append("Error - API key not included in request")
		elif request_json['api_key'] != "secretsarenofun":
			error_list.append("invalid api key!")
		else:
			success_list.append("huzzah!!")

	check_api_key(request_json, succ, errs)

	logging.warn(f.escape(request.headers))
	logging.warn(f.escape(request.referrer))
	logging.warn(f.escape(request.remote_addr))
	logging.warn(f.escape(request.user_agent))

	response_body = []

	if len(errs):
		response_body = errs
	else: 
		response_body = succ

	return f.make_response(f.jsonify(response_body))



# Check JSON Body for key
# Query DB 
# Return response to Salesforce


### FULL THING!!
## Receive request and parse JSON


## Check JSON for key, abort if not there



## Check JSON for required values



## Create DB Lookup keys 




## Do DB Queries




## Do DVT Math




## Return response



### 



def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(escape(name))