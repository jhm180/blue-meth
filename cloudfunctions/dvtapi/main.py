import flask as f
import logging
import dvtutils as du
import os
from psycopg2 import OperationalError
from psycopg2.pool import SimpleConnectionPool

pg_config = {
  'user': os.environ.get('DB_USER'),
  'password': os.environ.get('DB_PW'),
  'dbname': os.environ.get('DB_NAME')
}

# Connection pools reuse connections between invocations, and handle dropped or expired connections automatically.
pg_pool = None
#to do - keep exausting conn pool... need to correct implmentation

# helper function for conneting
def db_connect(host):
    global pg_pool
    pg_config['host'] = host
    pg_pool = SimpleConnectionPool(1, 1, **pg_config)


def dvt_api_staging(request):
# instantiate some values 
    errs = []

## Receive request and parse JSON, abort if no JSON found
    request_json = request.get_json(silent=True)
    if not request_json:
        return str('ERROR: No json detected in body of request. (Note: all values are case sensitive)')

## Check JSON for api key, abort if missing or invalid
    du.check_api_key(request_json, errs)
    if len(errs) > 0:
        return ('ERROR: '+str(errs)+' (Note: all values are case sensitive)')
   
## Check JSON for required keys and data validity, abort if incorrect
    du.check_json_values(request_json, errs)
    if len(errs) > 0:
        return ('ERROR: '+str(errs)+' (Note: all values are case sensitive)')

## Create DB Lookup keys 
    weight_key, shape_disc_weight_group, discounts_weight_group, rap_price_list_weight_key = du.get_curve_key(request_json)
    shape_key, rap_price_list_shape_key = du.get_shape_key(request_json)
    discount_group_key_suffix = du.get_discount_group_key(request_json)
    price_param_key = '{0}_{1}_{2}_{3}'.format(shape_key, request_json['color'], request_json['clarity'], weight_key)
    shape_discount_key = '{0}_{1}_{2}_{3}'.format(request_json['color'], request_json['clarity'], shape_disc_weight_group, request_json['shape'])
    discount_key = '{0}_{1}_{2}_{3}_{4}'.format(shape_key, discounts_weight_group, request_json['color'], request_json['clarity'], discount_group_key_suffix) 
    rap_price_list_key = '{0}_{1}_{2}_{3}'.format(rap_price_list_shape_key, request_json['color'], request_json['clarity'], rap_price_list_weight_key)


## Do DB Queries
    global pg_pool
    # Initialize the pool lazily, in case SQL access isn't needed for this
    # GCF instance. Doing so minimizes the number of active SQL connections,
    # which helps keep your GCF instances under SQL connection limits.
    if not pg_pool:
        try:
            db_connect(f'/cloudsql/wpdvt-228113:us-central1:wpdvt-db')
        except OperationalError:
            # If production settings fail, use local development ones
            db_connect('localhost')

    with pg_pool.getconn().cursor() as cursor:
        cursor.execute('SELECT * FROM dvt.priceparams WHERE dvt.priceparams.paramkey = %s', (price_param_key,))
        price_params = cursor.fetchone()
        cursor.close()
        #pg_pool.close()
        return str(price_params) +" ---- "+ str(shape_discount_key) +" ---- "+ str(discount_key) +" ---- "+ str(rap_price_list_key)


## Do DVT Math




## Return response



### 
