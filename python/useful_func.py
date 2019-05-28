import pandas as pd
import numpy as np
from scipy import stats
from itertools import (takewhile,repeat)

def colName_replace(df, old, new):
    # Replace column name across with certain element
    '''
    Param:
        old: string, old part of the column name want to be replaced
        new: string
    Return:
        dataframe
    '''
    for i in range(0, len(df.columns)):
        df = df.rename(columns = {df.columns[i]:df.columns[i].replace(old,new)})
    return df

def rsquared(x, y):
    # Return R^2 where x and y are array-like
    '''
    Param:
        x: array
        y: array
    Return:
        R-square value
    '''
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return r_value**2
    
def proc_freq(df, group, val):
    '''
    Param:
        df: dataframe
        group: string of the column name to be table variable (SAS syntax)
        val: string of the column name to be var
    Return:
        print of the result table
    '''
    total_count = df.shape[0]
    count = df.groupby(group)[val].count()
    mix = df.groupby(group)[val].count() / df.shape[0]
    foo = pd.concat([count.rename("Count"), mix.rename("Mix")], axis = 1)
    bar = pd.DataFrame([[total_count, 1]], columns = ['Count', 'Mix'], index = ['Total'])
    
    print(pd.concat([foo, bar], axis = 0))
    
def proc_means(df, group, val):
    '''
    Param:
        df: dataframe
        group: string of the column name to be group variable (SAS syntax)
        val: string of the column name to be var (SAS syntax)
    Return:
        print of the result table
    '''
    total_count = df.shape[0]
    total_sum = df[val].sum()
    total_mean = df[val].mean()
    count = df.groupby(group)[val].count()
    Sum = df.groupby(group)[val].sum()
    Mean = df.groupby(group)[val].mean()
    foo = pd.concat([count.rename("Count"), Sum.rename("Sum"), Mean.rename("Mean")], axis = 1)
    bar = pd.DataFrame([[total_count, total_sum, total_mean]], columns = ['Count', 'Sum', 'Mean'], index = ['Total'])
    
    print(pd.concat([foo, bar], axis = 0))

# Use to read number of rows of the file
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

# date column transformation
def date_format(df):
    col = df.filter(regex='date').columns
    for i in col:
        df[i] = pd.to_datetime(df[i], dayfirst=True, format='%Y%m%d')
    return df

# cut first x rows from a huge file
def chop_small_file(infile, outfile, num_records):
    '''
    infile: input file path name
    outfile: output file path name
    num_records: # want to keep
    '''
    with open(outfile, 'w') as f2:
        with open(infile) as f1:
            for i, line in enumerate(f1):
                if i < num_records:
                    f2.write(line)
                else:
                    break
# save a dict with pandas dataframe in it
def saver(dictex):
    for key, val in dictex.items():
        val.to_csv("data/data_{}.csv".format(str(key)))

    with open("data/keys.txt", "w") as f: #saving keys to file
        f.write(str(list(dictex.keys())))

def loader():
    """Reading data from keys"""
    with open("data/keys.txt", "r") as f:
        keys = eval(f.read())

    dictex = {}    
    for key in keys:
        dictex[key] = pd.read_csv("data/data_{}.csv".format(str(key)))

