
def colName_replace(df, old, new):
    # Replace column name across with certain element
    for i in range(0, len(df.columns)):
        df = df.rename(columns = {df.columns[i]:df.columns[i].replace(old,new)})
    return df

def rsquared(x, y):
    # Return R^2 where x and y are array-like
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return r_value**2
    
def proc_freq(df, Class, Val):
    total_count = df.shape[0]
    count = df.groupby(Class)[Val].count()
    mix = df.groupby(Class)[Val].count() / df.shape[0]
    foo = pd.concat([count.rename("Count"), mix.rename("Mix")], axis = 1)
    bar = pd.DataFrame([[total_count, 1]], columns = ['Count', 'Mix'], index = ['Total'])
    
    print pd.concat([foo, bar], axis = 0)
    
def proc_means(df, Class, Val):
    total_count = df.shape[0]
    total_sum = df[Val].sum()
    total_mean = df[Val].mean()
    count = df.groupby(Class)[Val].count()
    Sum = df.groupby(Class)[Val].sum()
    Mean = df.groupby(Class)[Val].mean()
    foo = pd.concat([count.rename("Count"), Sum.rename("Sum"), Mean.rename("Mean")], axis = 1)
    bar = pd.DataFrame([[total_count, total_sum, total_mean]], columns = ['Count', 'Sum', 'Mean'], index = ['Total'])
    
    print pd.concat([foo, bar], axis = 0)

# Use to read number of rows of the file
from itertools import (takewhile,repeat)

def rawincount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )

# Compare two dataframe
import pandas as pd
import numpy as np

def compare_two_dfs(input_df_1, input_df_2):
    df_1, df_2 = input_df_1.copy(), input_df_2.copy()
    ne_stacked = (df_1 != df_2).stack()
    changed = ne_stacked[ne_stacked]
    changed.index.names = ['id', 'col']
    difference_locations = np.where(df_1 != df_2)

    changed_from = df_1.values[difference_locations]

    changed_to = df_2.values[difference_locations]

    df = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)
    return df
