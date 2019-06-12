import numpy as np

# preprocess for production
def preprocess(trips_in):
    trips = trips_in.copy(deep=True)
    trips.fare_amount = trips.fare_amount + trips.tolls_amount
    del trips['tolls_amount']
    del trips['total_amount']
    del trips['trip_distance']
    del trips['pickup_datetime']
    qc = np.all([\
               trips['pickup_longitude'] > -78, \
               trips['pickup_longitude'] < -70, \
               trips['dropoff_longitude'] > -78, \
               trips['dropoff_longitude'] < -70, \
               trips['pickup_latitude'] > 37, \
               trips['pickup_latitude'] < 45, \
               trips['dropoff_latitude'] > 37, \
               trips['dropoff_latitude'] < 45, \
               trips['passenger_count'] > 0,
              ], axis=0)
    return trips[qc]

tripsqc = preprocess(trips)
tripsqc.describe()

# split data
shuffled = tripsqc.sample(frac=1)
trainsize = int(len(shuffled['fare_amount']) * 0.70)
validsize = int(len(shuffled['fare_amount']) * 0.15)

df_train = shuffled.iloc[:trainsize, :]
df_valid = shuffled.iloc[trainsize:(trainsize+validsize), :]
df_test = shuffled.iloc[(trainsize+validsize):, :]

# write out to csv
def to_csv(df, filename):
    outdf = df.copy(deep=False)
    outdf.loc[:, 'key'] = np.arange(0, len(outdf)) # rownumber as key
    # reorder columns so that target is first column
    cols = outdf.columns.tolist()
    cols.remove('fare_amount')
    cols.insert(0, 'fare_amount')
    print (cols)  # new order of columns
    outdf = outdf[cols]
    outdf.to_csv(filename, header=False, index_label=False, index=False)

to_csv(df_train, 'taxi-train.csv')
to_csv(df_valid, 'taxi-valid.csv')
to_csv(df_test, 'taxi-test.csv')
