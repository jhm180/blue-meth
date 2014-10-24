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

ADD = 1
REMOVE = 2
READD = 3
PRICE_CHANGE = 4

DATA_PATH = '/home/oliver/rapnet_data'
CACHE_PATH = '/home/oliver/rapnet_cache'
COL_NAMES = ['LotNum', 'Owner', 'Shape', 'Carat', 'Color', 'Clarity', 'Cut Grade', 'Price', 'PctRap',
 'Cert', 'Depth', 'Table', 'Girdle', 'Culet', 'Polish', 'Sym', 'Fluor', 'Meas', 'Comment',
 'NumStones', 'CertNum', 'StockNum', 'Make', 'Date', 'City', 'State', 'Country', 'Image']

def read_daily_file(file_date):
    compression = None
    daily_file = path.join(DATA_PATH, 'Rapnet_{0}_Main.csv'.format(file_date))
    if not path.exists(daily_file):
        daily_file = daily_file + '.gz'
        compression = "gzip"
    if not path.exists(daily_file):
        return []
    try:
        return read_csv(daily_file, compression = compression, names = COL_NAMES, header = 0,
                    #dtype = {'Owner':str, 'CertNum':str},
                    engine = 'python')
    except EOFError:
        print 'bad file {0}; renaming'.format(daily_file)
        shutil.move(daily_file, daily_file + '.bad')
        return []

# don't load fake cert nums
bad_certs = { '123456789', '', '1234567890', '0' }

def days_on_market(df):
    # grp here is all rows matching the same (owner,certnum) key
    # here we arrange by date
    intervals = []
    # the all_df frame is already sorted by date, so no need to re-sort here if it's the same df
    #df.sortlevel(level='event_day', inplace=True)
    grpd = df.groupby(level=['Owner','CertNum'])
    t1 = datetime.now()
    for grpname, vals in grpd:
        # loop for each event_type/date entry in this stone's dataframe
        # name is the original multiindex of the row prior to the groupby operation
        for name, valseries in vals.iterrows(): 
            # looks back through all events for a given stone and generates
            # a new row for each interval on the market, indexed by certnum and owner
            # (the group name, or label
            et = name[0]
            #print et
            if et == ADD or et == READD:
                date_added = name[3] 
            elif et == REMOVE:
                if date_added != None:
                    date_removed = name[3]
                    intervals.append([date_added, date_removed, grpname])
                                    #index = pd.MultiIndex(levels = [grpname[0], grpname[1], date_removed])))

    tuples = [iv[2] for iv in intervals]
    return pd.DataFrame([iv[:2] for iv in intervals], index = pd.MultiIndex.from_tuples(tuples), columns = ['added','removed'])

def filter_data(df):
    indices = []
    for k, grpdf in df.groupby(['Owner','CertNum']):
        if len(grpdf) == 1:
            indices.append(grpdf.index[0])
        elif not k[1] in bad_certs:
            # we were dropping a lot of dupes, so instead i'm
            # just adding the one w/ the highest lot num
            indices.append(grpdf.LotNum.idxmax())
    nodupes = df.loc[indices]
    #dupes = df.loc[df.index - indices]
    if len(df) - len(nodupes) > 0:
        print 'Filtering: dropped {0} of {1} rows'.format(len(df) - len(nodupes), len(df))
    stones = nodupes[[c for c in COL_NAMES if not c in {'CertNum','Owner'}]]
    stones.index = pd.MultiIndex.from_tuples([(owner, cert) for owner, cert in nodupes[['Owner','CertNum']].values],
                                             names = ['Owner', 'CertNum'])
    return stones

def cache_records(records, active, file_date):  
    now = datetime.now()
    atts = {
          'file_date': file_date,
          'records': records,
          'active':active
        }
    pd.Series(atts).to_pickle(path.join(CACHE_PATH, 'rapnet.pkl'))
    print 'cache write took {0}'.format(datetime.now() - now)
    #s = HDFStore(path.join(CACHE_PATH, 'rapnet.h5'), complevel=9, complib='blosc')
    #s['records'] = records
    #s['active'] = active
    #s['attributes'] = pd.Series({'file_date':file_date})
    
def load_cache():
    now = datetime.now()
    #h5path = path.join(CACHE_PATH, 'rapnet.h5')
    #if path.exists(h5path):
    #    s = H5Store(h5path)
    #    atts = s['attributes'].to_dict()
    #    return s['records'], s['active'], atts['file_date']
    pklpath = path.join(CACHE_PATH, 'rapnet.pkl')
    if path.exists(pklpath):
        s = pd.read_pickle(pklpath).to_dict()
        print 'cache load took {0}'.format(datetime.now() - now)
        return s['records'], s['active'], s['file_date']
    return [], [], []

def gen_file_dates(start_day):
    oneday = timedelta(1)
    today = datetime.today()
    #today = datetime.strptime('20130304', '%Y%m%d')
    cur_day = start_day
    while cur_day <= today:
        yield cur_day
        cur_day = cur_day + oneday
        
def get_latest(grp):
    grp.sortlevel(level='event_day', inplace=True, ascending = False)
    return grp.iloc[0]

def build_cache():
    all_records, prev, prev_day = load_cache()
    first_day = datetime(2013,3,3)
    if prev_day:
        first_day = datetime.strptime(prev_day, '%Y%m%d') + timedelta(1)
        print 'build_cache starting after previous load date', prev_day
    i = 0
    def reindex(idx_day, idx_event, df):
        df.index = pd.MultiIndex.from_tuples([(idx_event, owner, cert, idx_day) for owner, cert in df.index],
                                             names = ['event_type','Owner','CertNum','event_day'])
            
    file_date = None
    for cur_day in gen_file_dates(first_day):
        file_date = cur_day.strftime('%Y%m%d')
        now = datetime.now()
        df = read_daily_file(file_date)
        if len(df) == 0:
            continue
        print 'processing file for {0}...'.format(file_date),
        active = filter_data(df)
        if len(prev):
            new_stones = active.loc[active.index - prev.index]
            kept_stones = prev.loc[active.index & prev.index]
            readds = []
            if len(new_stones):           
                # cross section of data - we only want things were previously 
                # removed, to see if any of the new_stones are actually re-adds
                all_removals = []
                try:
                    all_removals = all_records.xs(REMOVE, level = 'event_type')
                except KeyError:
                    pass
                if len(all_removals):
                    prev_removals = all_removals.groupby(level=['Owner','CertNum']).apply(get_latest)
                    if len(prev_removals):
                        readds = new_stones.loc[new_stones.index & prev_removals.index]
                        if len(readds):
                            newonly = new_stones.index - readds.index
                            if len(newonly):
                                new_stones = new_stones.loc[newonly]
                            else:
                                new_stones = []

            if len(new_stones):
                reindex(cur_day, ADD, new_stones)
                all_records = pd.concat([all_records, new_stones])

            if len(readds):
                reindex(cur_day, READD, readds)
                all_records = pd.concat([all_records, readds])
                
            # join the stones not removed w/ the current load to see what's changed
            joined_px = pd.merge(kept_stones, active, left_index = True, right_index = True)

            # see if any prices have changed
            px_changes = active.loc[joined_px[(joined_px.Price_x != joined_px.Price_y) & ~(np.isnan(joined_px.Price_y))].index]
            if len(px_changes):
                reindex(cur_day, PRICE_CHANGE, px_changes)
                all_records = pd.concat([all_records, px_changes])

            # see what's been removed
            removals = prev.loc[prev.index - active.index]
            if len(removals):
                reindex(cur_day, REMOVE, removals)
                all_records = pd.concat([all_records, removals])
                
            print '{0} new stones, {1} removals, {2} price changes, {3} readds'.format(
                len(new_stones), len(removals), len(px_changes), len(readds))
        else:
            # create all_records w/ multiindex: event_date, event_type, certnum
            all_records = active.copy()
            reindex(cur_day, ADD, all_records)
        cache_records(all_records, active, file_date)
        prev = active
        gc.collect()
        print 'took {0}'.format(datetime.now() - now)
    return all_records, prev, file_date

if __name__ == "__main__":
   build_cache()
