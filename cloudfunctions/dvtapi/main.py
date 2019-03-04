import flask as f
import logging
import dvtutils as du
import os
from psycopg2 import OperationalError
from psycopg2.pool import SimpleConnectionPool

# TODO(developer): specify SQL connection details

pg_config = {
  'user': os.environ.get('DB_USER'),
  'password': os.environ.get('DB_PW'),
  'dbname': os.environ.get('DB_NAME')
}

# Connection pools reuse connections between invocations,
# and handle dropped or expired connections automatically.
pg_pool = None
# helper function for conneting

def db_connect(host):
    global pg_pool
    pg_config['host'] = host
    pg_pool = SimpleConnectionPool(1, 1, **pg_config)


def dvt_api_staging(request):
    global pg_pool
    request_json = request.get_json(silent=True)
    errs = []
    succ = []

    # Initialize the pool lazily, in case SQL access isn't needed for this
    # GCF instance. Doing so minimizes the number of active SQL connections,
    # which helps keep your GCF instances under SQL connection limits.
    
    def check_api_key(request_json, success_list, error_list):
        try:
            if request_json['api_key'] != "secretsarenofun":
                error_list.append("invalid api key!")
            else:
                success_list.append("huzzah!!")
        except KeyError:
            error_list.append("api_key not found in body of request")

    check_api_key(request_json, succ, errs)


    if not pg_pool:
        try:
            db_connect(f'/cloudsql/wpdvt-228113:us-central1:wpdvt-db')
        except OperationalError:
            # If production settings fail, use local development ones
            db_connect('localhost')

    # Remember to close SQL resources declared while running this function.
    # Keep any declared in global scope (e.g. pg_pool) for later reuse.

    param_key = du.get_price_params(request_json)
    logging.warn(str(param_key))

    with pg_pool.getconn().cursor() as cursor:
        cursor.execute("SELECT * FROM dvt.priceparams WHERE dvt.priceparams.paramkey = %s", (param_key,))
        price_params = cursor.fetchone()
        return price_params


# Google sample code - https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/functions/helloworld/main.py
# HTTP Request documentation - https://cloud.google.com/functions/docs/writing/http

### FULL THING!!
## Receive request and parse JSON


## Check JSON for key, abort if not there



## Check JSON for required values



## Create DB Lookup keys 




## Do DB Queries




## Do DVT Math




## Return response



### 
