import pandas as pd
from os import path
from datetime import datetime, timedelta
from pandas.io.parsers import read_csv
import numpy as np
import gc
# from pandas.io.pytables import HDFStore
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

# actual headers for new format:
# Seller Name,RapNet Account ID,Name Code,Shape,Weight,Color,Clarity,Cut,Polish,
# Symmetry,Fluorescence Color,Measurements,Lab,Certificate Number,Stock Number,
# Price Per Carat,Price Percentage,Cash Price Per Carat,Cash Price Percentage,
# Depth,Table,Girdle,Culet,Culet Size,Culet Condition,
# City,State,Country,Certificate URL,Image URL,Depth Percent,Diamond ID

COL_NAMES_20141205 = [
'SellerName','RapnetAccount','Owner','Shape','Carat','Color','Clarity','Cut Grade','Polish',
'Sym','Meas','Cert','CertNum','StockNum',
'Price','PctRap',
'Depth','Table','Girdle','Culet','Culet Size','Culet Condition',
'City','State','Country','Certificate URL','Image','Depth Percent','LotNum','CertNum1','Fluor'
]

COL_NAMES_20141218 = [
'SellerName','RapnetAccount','Owner','Shape','Carat','Color','Clarity','Cut Grade','Polish',
'Sym','Meas','Cert','CertNum','StockNum',
'Price','PctRap','Cash Price Per Carat','Cash Price Percentage',
'Depth','Table','Girdle','Culet','Culet Size','Culet Condition',
'City','State','Country','Certificate URL','Image','Depth Percent','LotNum','CertNum1','Fluor'
]
#
DOWNLOADED_COL_NAMES_20150104 = """Seller Name,RapNet Account ID,Name Code,Shape,Weight,Color,Clarity,Cut,Polish,
Symmetry,Fluorescence Color,Fluorescence Intensity,Measurements,Meas Length,
Meas Width,Meas Depth,Lab,Certificate Number,Stock Number,Price Per Carat,
Price Percentage,Depth,Table,Girdle,Culet,Culet Size,Culet Condition,
Crown,Pavilion,City,State,Country,Number of Diamonds,Certificate URL,
Image URL,Date Updated,Pavilion Angle,Table Percent,
Supplier country,Depth Percent,Crown Angle,Crown Height,Diamond ID"""

COL_NAMES_20150104 = [
'SellerName','RapnetAccount','Owner','Shape','Carat','Color','Clarity','Cut Grade','Polish',
'Sym','FlourColor','Fluor','Meas','Meas Len','MeasWidth','MeasDepth','Cert','CertNum','StockNum',
'Price','PctRap',
'DepthStr','TableStr','Girdle','Culet','Culet Size','Culet Condition','Crown','Pavilion',
'City','State','Country','NumStones','Certificate URL','Image','DateUpdated','Pavilion Angle',
'Table','SupplierCountry','Depth','Crown Angle','CrownHeight','LotNum'
]

DOWNLOADED_COL_NAMES_20170627 = """Seller Name,RapNet Account ID,Name Code,Shape,Weight,Color,Clarity,Cut,Polish,
Symmetry,Fluorescence Color,Fluorescence Intensity,Measurements,Meas Length,
Meas Width,Meas Depth,Lab,Certificate Number,Stock Number,Price Per Carat,
Price Percentage,Depth,Table,Girdle,Culet,Culet Size,Culet Condition,
Crown,Pavilion,City,State,Country,Number of Diamonds,Certificate URL,
Image URL,Date Updated,Pavilion Angle,Table Percent,
Supplier country,Depth Percent,Crown Angle,Crown Height,Diamond ID"""

COL_NAMES_20170627 = [
'SellerName','RapnetAccount','Owner','Shape','Carat','Color','Clarity','Cut Grade','Polish',
'Sym','FlourColor','Fluor','Meas','Meas Len','MeasWidth','MeasDepth','Cert','CertNum','StockNum',
'Price','PctRap',
'DepthStr','TableStr','Girdle','Culet','Culet Size','Culet Condition','Crown','Pavilion',
'City','State','Country','NumStones','Certificate URL','Image','DateUpdated','Pavilion Angle',
'Table','SupplierCountry','Depth','Crown Angle','CrownHeight','LotNum'
]

USE_COLS = ['LotNum', 'Owner', 'Shape', 'Carat', 'Color', 'Clarity', 'Cut Grade', 'Price', 'PctRap',
 'Cert', 'Depth', 'Table', 'Girdle', 'Culet', 'Polish', 'Sym', 'Fluor', 'Meas',
 'CertNum', 'StockNum', 'City', 'State', 'Country', 'Image']

NEW_FMT_DATE = datetime(2014, 12, 4)
NEW_FMT_DATE2 = datetime(2014, 12, 17)
NEW_FMT_DATE3 = datetime(2015, 1, 3)
NEW_FMT_DATE4 = datetime(2017, 6, 27)

def parse_pct(f):
    fv = f.strip()
    if len(fv) == 0:
        return None
    if fv[-1] == '%':
        fv = fv[:-1]
    return np.float64(fv)

def read_daily_file(cur_day):
    file_date = cur_day.strftime('%Y%m%d')
    compression = None
    daily_file = path.join(DATA_PATH, 'Rapnet_{0}_Main.csv'.format(file_date))
    if not path.exists(daily_file):
        daily_file = daily_file + '.gz'
        compression = "gzip"
    if not path.exists(daily_file):
        return []
    try:
        if cur_day > NEW_FMT_DATE4:
            print "loading date {0} with new format 4".format(file_date)
            df = read_csv(daily_file, compression = compression, header = 0,
                        engine = 'python')
            names = [n.strip() for n in DOWNLOADED_COL_NAMES_20170627.split(',')]
            col_dict = dict(zip(names, COL_NAMES_20170627))
            df.drop([n for n in df.columns if not n in names], 1, inplace = True)
            df.rename(columns = col_dict, inplace = True)
            return df
        elif cur_day > NEW_FMT_DATE3:
            print "loading date {0} with new format 3".format(file_date)
            return read_csv(daily_file, compression = compression, names = COL_NAMES_20150104, header = 0,
                        engine = 'python')
        elif cur_day > NEW_FMT_DATE2:
            print "loading date {0} with new format 2".format(file_date)
            return read_csv(daily_file, compression = compression, names = COL_NAMES_20141218, header = 0,
                        converters = {'Table':parse_pct, 'Depth':parse_pct}, engine = 'python')
        elif cur_day > NEW_FMT_DATE:
            print "loading date {0} with new format".format(file_date)
            return read_csv(daily_file, compression = compression, names = COL_NAMES_20141205, header = 0,
                        converters = {'Table':parse_pct, 'Depth':parse_pct}, engine = 'python')
        else:
            return read_csv(daily_file, compression = compression, names = COL_NAMES, header = 0,
                        engine = 'python')[USE_COLS]
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
    stones = nodupes[[c for c in USE_COLS if not c in {'CertNum','Owner'}]]
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

def load_cache(cachepath = CACHE_PATH):
    now = datetime.now()
    #h5path = path.join(CACHE_PATH, 'rapnet.h5')
    #if path.exists(h5path):
    #    s = H5Store(h5path)
    #    atts = s['attributes'].to_dict()
    #    return s['records'], s['active'], atts['file_date']
    pklpath = path.join(cachepath, 'rapnet.pkl')
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

def read_latest_file():
    d = datetime.today()
    df = read_daily_file(d)
    while len(df) == 0:
        d = d - timedelta(days=1)
        df = read_daily_file(d)
    return filter_data(df), d.strftime('%Y%m%d')

def get_latest(grp):
    grp.sortlevel(level='event_day', inplace=True, ascending = False)
    return grp.iloc[0]

def build_cache():
    all_records, prev, prev_day = load_cache()
    first_day = datetime(2013,3,3)
    if prev_day:
        first_day = datetime.strptime(prev_day, '%Y%m%d') + timedelta(1)
        print 'build_cache starting after previous load date', prev_day
    def reindex(idx_day, idx_event, df):
        df.index = pd.MultiIndex.from_tuples([(idx_event, owner, cert, idx_day) for owner, cert in df.index],
                                             names = ['event_type','Owner','CertNum','event_day'])

    file_date = None
    for cur_day in gen_file_dates(first_day):
        now = datetime.now()
        df = read_daily_file(cur_day)
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
