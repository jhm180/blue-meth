import flask as f
import logging
import dvtutils as du
import os
from psycopg2 import OperationalError
from psycopg2.pool import SimpleConnectionPool

# TOMORROW - FINISH value checker, find a way to abort and return error messages after json parsing, api key check an value check

pg_config = {
  'user': os.environ.get('DB_USER'),
  'password': os.environ.get('DB_PW'),
  'dbname': os.environ.get('DB_NAME')
}

# Connection pools reuse connections between invocations, and handle dropped or expired connections automatically.
pg_pool = None
# helper function for conneting

def db_connect(host):
    global pg_pool
    pg_config['host'] = host
    pg_pool = SimpleConnectionPool(1, 1, **pg_config)


def dvt_api_staging(request):
# instantiate some values 
    errs = []
    succ = []

## Receive request and parse JSON
    #to do - error handling if cannot find json request + abort    
    request_json = request.get_json(silent=True)
    if not request_json:
        return str("ERROR: No json detected in body of request")

## Check JSON for api key, abort if missing or invalid
    du.check_api_key(request_json, errs)
    if len(errs) > 0:
        return ("ERROR: "+str(errs))
   
## Check JSON for required values
    du.check_json_values(request_json, errs)
    if len(errs) > 0:
        return ("ERROR: "+str(errs))

## Create DB Lookup keys 
    param_key = du.get_price_params(request_json)


## Do DB Queries
    #connect to DB
    if not pg_pool:
        try:
            db_connect(f'/cloudsql/wpdvt-228113:us-central1:wpdvt-db')
        except OperationalError:
            # If production settings fail, use local development ones
            db_connect('localhost')

    with pg_pool.getconn().cursor() as cursor:
        cursor.execute("SELECT * FROM dvt.priceparams WHERE dvt.priceparams.paramkey = %s", (param_key,))
        price_params = cursor.fetchone()
        return str(price_params)


## Do DVT Math




## Return response



### 
