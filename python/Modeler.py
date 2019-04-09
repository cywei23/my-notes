import pandas as pd
import numpy as np
import csv
import re
import decimal
import math
import os
import re
import pickle
import time
import json

import matplotlib.pyplot as plt

from sklearn import metrics
from scipy import stats

def identifier(df, manual_drop_string, sample_size = 10000, max_level_to_OHE = 8, max_to_na_median = 0.75):
    # df: dataframe for identifying column transfomration groups
    # manual_drop_string: dependent variables and other variables not to be included in predictor
    #    transformation
    # sample_size: sample size for identifier
    # max_level_to_OHE: maximum levels for One-Hot-Encode transformation
    # max_to_na_median: maximum NA percentage to use median as mising value imputation
    
    # sample
    df = df.sample(n = sample_size, random_state = 1111).reset_index(drop = True)
    
    # 1. manual drop
    column_list_manual_drop = manual_drop_string.split()
    df = df.drop(column_list_manual_drop, axis = 1)
    
    # 2. mixed string and numeric
    numeric_selection = [bool(re.search(r'\d', ''.join([str(x) for x in df.loc[:,col].values if not pd.isnull(x)]))) for col in df.columns]
    alpha_selection = [bool(re.search(r'[a-zA-Z]', ''.join([str(x) for x in df.loc[:,col].values if not pd.isnull(x)]))) for col in df.columns]
    wspace_selection = [bool(re.search(r'\s', ''.join([str(x) for x in df.loc[:,col].values if not pd.isnull(x)]))) for col in df.columns]
    selection = (np.array(numeric_selection) & np.array(alpha_selection)) & ~np.array(wspace_selection)

    alpha_num_columns = list(df.loc[:,selection].columns)

    column_list_alpha_num = alpha_num_columns
    df = df.drop(column_list_alpha_num, axis = 1)
    
    # 3.1 Drop all NA columns
    column_list_drop_all_na = list(set(df.columns) - set(df.dropna(axis=1, how = 'all').columns))
    df = df.drop(column_list_drop_all_na, axis = 1)
    
    # 3.2 ID
    cardinality = [[col, len(df[col].unique())] for col in df.columns]
    cardinality = pd.DataFrame(cardinality)
    cardinality.columns = 'column card'.split()

    column_list_id = cardinality[cardinality['card'] == sample_size]
    column_list_id = column_list_id['column'].values.tolist()

    df = df.drop(column_list_id, axis = 1)
    
    # 4 convert from dates to "days since x"
    # To do: need to add other date type and code out the format to transform
    date_selection = [bool(re.search(r'(\d+-\d+-\d+)', ''.join([str(x) for x in df.loc[0:99,col].values if not pd.isnull(x)]))) for col in df.columns]
    column_list_date = list(df.loc[:,date_selection].columns)

    df = df.drop(column_list_date, axis = 1)
    
    # 5 (numeric & string) OHE for level under 8 (default)
    cardinality = [[col, len(df[col].unique())] for col in df.columns]
    cardinality = pd.DataFrame(cardinality)
    cardinality.columns = 'column card'.split()
    
    column_list_ohe = cardinality[cardinality['card'] <= max_level_to_OHE]
    column_list_ohe = column_list_ohe['column'].values.tolist()

    df = df.drop(column_list_ohe, axis = 1)
    
    # 6. Freqeuncy count for Many level Strings
    #
    #general rule:
    #remaining categorical variables (pandas "object" data type) after the previous step,
    #namely they have cardinality >= 10
    df_obj = df.loc[:,df.dtypes == np.object] 
    df_obj.columns
    column_list_count_average =  list(df_obj.columns)

    df = df.drop(column_list_count_average, axis = 1)

    # 7 fill NA with 0 predictors
    #large number (>75%) of NAs on a column that has cardinality = 1 (simply an indicator of an event)

    df_num = df.loc[:,df.dtypes != np.object] 
    foo = df_num.isnull().sum()
    bar = pd.DataFrame([foo.index, foo.values]).T
    bar.columns = 'column na_count'.split()
    selection = bar.na_count / sample_size >= max_to_na_median
    foobar = bar[selection]
    foobar.sort_values('na_count', ascending = False).head()
    column_list_na0_predictors = list(foobar.column.values)

    df = df.drop(column_list_na0_predictors, axis = 1)
    
    # 8 fill NA with median
    #any remaining numeric variables (they should fall into the category of numeric with cardinality > 9 and <25% NA) 

    selection = (bar.na_count / sample_size < max_to_na_median) & (bar.na_count > 0)
    foobar = bar[selection]
    column_list_na_median = list(foobar.column.values)
    
    df = df.drop(column_list_na_median, axis = 1)

    # 9. no transformation needed
    #all "surviving" variables after the preceding steps (should be all numeric with no NAs) 
    #should be treated similarly to fill NA with median (seems best) or fill NA with -1 (saves computation)?
    column_list_no_tans = list(df.columns)
    
    list_names = \
    """column_list_count_average
    column_list_date
    column_list_drop_all_na
    column_list_id
    column_list_manual_drop
    column_list_na_median
    column_list_no_tans
    column_list_ohe
    column_list_alpha_num
    column_list_na0_predictors""".split()

    column_lists = \
    [column_list_count_average,
    column_list_date,
    column_list_drop_all_na,
    column_list_id,
    column_list_manual_drop,
    column_list_na_median,
    column_list_no_tans,
    column_list_ohe,
    column_list_alpha_num,
    column_list_na0_predictors]

    column_count = \
    [len(column_list_count_average),
    len(column_list_date),
    len(column_list_drop_all_na),
    len(column_list_id),
    len(column_list_manual_drop),
    len(column_list_na_median),
    len(column_list_no_tans),
    len(column_list_ohe),
    len(column_list_alpha_num),
    len(column_list_na0_predictors)]

    data_type_dictionary = dict(zip(list_names, column_lists))    
    data_type_count_dictionary = dict(zip(list_names, column_count))
    
    print(data_type_count_dictionary)
    
    return data_type_dictionary


class Transformer(object):
    def __init__(self, d):
        self._original_d = d
        self.d = self._original_d.copy()

        
        self.fitted = False
        self._fitting = False

        self._median_dictionary = None
        self._ohe_dictionary = None
        self._count_average_dictionary = None

        # self._extend_transform_dictionary()

    def fit_and_transform(self, df):
        # If someone runs fit_and_transform again, we need to go 
        # back to the original transform dictionary.
        if self.fitted:
            self.d = self._original_d.copy()

        self._fitting=True
        try:
            df = self.transform(df)
        except:
            raise
        else:
            self.fitted = True
        finally:
            self._fitting=False

        return df


    def transform(self, df):
        assert self._fitting or self.fitted

        ############################################################
        # Guarantee that columns match up the way we want them to
        ############################################################
        if self._fitting:
            # Remove columns from d that aren't in training set
            self._remove_deprecated_columns(df)
        # All columns in transform dictionary should be in the test set
        # TODO: Create a smarter check, which compares the original dictionary 
        # (minus the deprecated columns from the training run) to the test set columns.
        # This will probably be caught down the line, after some number of transformations have been run.
        # The problem with relying on that is that a lot of processing time will have been wasted.
        # We should try to catch as many of these problems as early as possible.
        # assert set(df.columns).issuperset(set(self._flat_d()))
        df = self._tf_drop(df)
        
        if self._fitting:
            assert set(self._flat_d()).issuperset(set(df.columns)) # There shouldn't be any columns in df.columns that aren't in transform dictionary

        if not self._fitting: df = self._drop_unknown_test_columns(df)


        ############################################################
        # Start transformations
        ############################################################

        if self._fitting: 
            self._add_alpha_cols_to_ohe()
            self._add_numer_cols_to_na_median(df)
        df = self._tf_alpha_num(df)
        df = self._tf_na0_predictors(df)

        # Date
        df = self._tf_date(df)
        if self._fitting: self.d['column_list_na_median'].extend(self.d['column_list_date'])

        # Replace na with median
        if self._fitting: self._median_dictionary = self._calc_median_dictionary(df)
        df = self._tf_na_median(df)

        # One-Hot-Encode
        if self._fitting: self._ohe_dictionary = self._calc_ohe_dictionary(df)
        df = self._tf_ohe(df)

        # Count and Average Transform
        if self._fitting: self._count_average_dictionary = self._calc_count_average_dictionary(df)
        df = self._tf_count_average(df)

        df = self._final_transform(df)

        return df

    def _drop_unknown_test_columns(self, df):
        cols_to_drop = list(set(df.columns) - set(self._flat_d()))
        df = df.drop(cols_to_drop, axis = 1)
        return df

    def _tf_drop(self, df):
        df = df.drop(self.d['column_list_drop_all_na'], axis = 1)
        df = df.drop(self.d['column_list_id'], axis = 1)
        #df = df.drop(self.d['column_list_manual_drop'], axis = 1)
        return df

    def _tf_date(self, df):
        for col in self.d['column_list_date']:
            df[col] = (pd.to_datetime(df[col], format = '%Y-%m-%d')\
                       - pd.to_datetime('2000-01-01', format = '%Y-%m-%d')\
                      ).dt.days
        return df

    def _tf_na0_predictors(self, df):
        for col in self.d['column_list_na0_predictors']:
            df.loc[df[col].isnull(), col] = -1
        return df


    def _final_transform(self, df):
        bar = df.isnull().sum()
        cols_fill_na0 = list(bar[bar != 0].index)

        for col in cols_fill_na0:
            df.loc[df[col].isnull(),col] = 0

        return df

    def _tf_ohe(self, df):
        tempdf = pd.DataFrame()
        for col in self.d['column_list_ohe']:
            dummy_col = df[col].dropna()
            # We convert numbers to ints because spark can't handle 
            # column names with dots (i.e. hot-encoded floats)
            if np.issubdtype(dummy_col.dtype, np.number):
                dummy_col = dummy_col.astype(int)

            # to keep the columns consistent between test and train, we filter
            # for values in self._ohe_dictionary
            dummy_col = dummy_col[dummy_col.isin(self._ohe_dictionary[col])]

            not_in_df = list(set(self._ohe_dictionary[col]) - set(dummy_col.unique()))

            for val in not_in_df:
                tempdf[col+'_ohe_'+str(val)] = 0

            tempdf = pd.concat([tempdf, pd.get_dummies(dummy_col, prefix = col + '_ohe')], axis = 1)
            
        df = pd.concat([df, tempdf], axis = 1)

        #drop old columns with have been one hot encoded
        df = df.drop(self.d['column_list_ohe'], axis = 1)
        return df

    def _calc_ohe_dictionary(self, df):
        ohe_dictionary = {}
        for col in self.d['column_list_ohe']:
            dummy_col = df[col].dropna()
            if np.issubdtype(dummy_col.dtype, np.number):
                dummy_col = dummy_col.astype(int)
                # this part is necessary because JSON only serializes normal python ints
                # (Not numpy ints)
                ohe_dictionary[col] = map(lambda val: int(val), list(dummy_col.unique()))
            else:
                ohe_dictionary[col] = list(dummy_col.unique())

        return ohe_dictionary

    def _calc_count_average_dictionary(self, df):
        count_average_dictionary = {}

        for col in self.d['column_list_count_average']:
                
            #fill NAs with a new category '-1'
            df[col] = df[col].fillna('-1')
            
            #calulate the frequency (counts) of the category and its average response rate (mean)  
            #means = df.groupby(col)['sales'].mean()
            counts = df.groupby(col)[col].count()
            
            #create a sub dictionary for each column 
            count_average_dictionary[col] = {}
            
            #within each column's sub-dictionary, create two dictionaries: mean and count
            #these record the mean and count for each category
            #count_average_dictionary[col]['mean'] = dict(zip(means.index,means.values))
            count_average_dictionary[col]['count'] = dict(zip(counts.index,counts.values))   
        return count_average_dictionary

    def _tf_count_average(self, df):
        #use the dictionary to extract the correct mean and count for each column
        #store these in new columns

        for col in self.d['column_list_count_average']:
            try:
                df[col] = df[col].fillna('-1')
                df[col+'_count'] = pd.Series()
                # df[col+'_mean'] = pd.Series()
                
                known_values = self._count_average_dictionary[col]['count'].keys()

                df.at[~df[col].isin(known_values), col] = '-1'

                for val in known_values:
                    df.at[df[col].astype(str).values==val, col+'_count'] = self._count_average_dictionary[col]['count'][val]
                    # df.at[df[col].astype(str).values==val, col+'_mean'] = self._count_average_dictionary[col]['mean'][val]

            except Exception as e:
                print('col: ', col)
                print(self.d['colulmn_list_count_average'])
                raise e

            
        #drop the original categorical columns
        df = df.drop(self.d['column_list_count_average'], axis = 1)

        return df

    def _calc_median_dictionary(self, df):
        median_dictionary = {}
        for col in self.d['column_list_na_median']:
            median = df[col].median()
            median_dictionary[col] = median
        return median_dictionary

    def _tf_na_median(self, df):
        for col in self.d['column_list_na_median']:
            col_median = self._median_dictionary[col]
            df.loc[df[col].isnull(),col] = col_median

        return df

    def _tf_alpha_num(self, df):
        #split the columns with a mix of alphabetical and numeric characters into two new columns
        #one column containing the characters, one the numerics
        for col in self.d['column_list_alpha_num']:
            
            df[col + '_alpha'] = [''.join(re.findall('[a-zA-Z]', str(x))) for x in df[col].values]
            #at a later date these numerics should be treated more carefuly 
            df[col + '_numer'] = [''.join(re.findall('\d', str(x))) for x in df[col].values]

        #convert the new *_numer columns as integers
        for col in self.d['column_list_alpha_num']:
            df[col + '_numer'] = pd.to_numeric(df[col + '_numer'], errors='coerce')
            #df[col + '_numer'] = df[col + '_numer'].astype(int)

        #discard old columns (we have extracted all their information)
        df = df.drop(self.d['column_list_alpha_num'], axis = 1)

        return df

    def _add_numer_cols_to_na_median(self, df):
        #add_to_median_list = [x + '_numer' for x in self.d['column_list_alpha_num']]
        #self.d['column_list_na_median'].extend(add_to_median_list)
        for col in self.d['column_list_alpha_num']:
            if col.find('_numer') > 0:
                if df[col].isnull().sum() / df.shape[0] > 0.75:
                    self.d['column_list_na_median'].extend(col)
                else:
                    self.d['column_list_na0_predictors'].extend(col)

    def _add_alpha_cols_to_ohe(self):
        add_to_ohe_list = [x + '_alpha' for x in self.d['column_list_alpha_num']]
        self.d['column_list_ohe'].extend(add_to_ohe_list)

    def _flat_d(self):
        '''Return up-to-date flattened list of all columns in transform dictionary'''
        return [column for category in self.d.values() for column in category]

    # def _extend_transform_dictionary(self):
        """Add new columns to transform dictionary d.
        (Should be part of transform dictionary creation in future)"""
        # self.d['column_list_na0_responses'].extend('sales_linc sales_linc_suv sales_mkc sales_mkx'.split()) 
        # self.d['column_list_na_median'].extend('number_of_persons_in_living_unit'.split())
        # self.d['column_list_drop_all_na'].extend('rn append'.split())

    def _remove_deprecated_columns(self, df):
        """Remove columns from transform dictionary d that are not in df."""
        to_be_removed = set(self._flat_d()) - set(df.columns)
        for key in self.d.keys():
            self.d[key] = [x for x in self.d[key] if not x in to_be_removed] # list(set(self.d[key]) - to_be_removed)


def roc_lift(fit, x_test, y_test, rank_count=10):
    # Function to show model evaluation - AUC and Lift by defined rank groups
    # fit: sklearn model fit
    # x_test: dataframe with x variables from test set
    # y_test: value with y from test set
    # rank_count: number of groups when showing cumulative lifts
    #scoring
    scores = fit.predict(x_test)
    fpr, tpr, thresholds = metrics.roc_curve(y_test, scores)
    
    #plotting roc
    print("(blue) ", fit, " roc:", metrics.auc(fpr,tpr))
    print("(red) random roc: 0.5")
    plt.plot(fpr,tpr,
             [0,1],[0,1])
    
    #Lift
    deciles = pd.DataFrame({'y' : y_test,
                            'yhat' : scores})

    decile_length = deciles.shape[0]//rank_count
    overall_rate = deciles['y'].mean()

    decile_event_cum = 0
    decile_count_cum = 0
    for decile_n in range(rank_count):

        decile_event = deciles.\
            sort_values('yhat', ascending= False).\
            reset_index(drop=True).\
            loc[decile_n*decile_length:(decile_n+1)*decile_length,'y'].\
            values.\
            sum()    

        decile_count = deciles.\
            reset_index(drop=True).\
            loc[decile_n*decile_length:(decile_n+1)*decile_length,'y'].\
            count()

        decile_event_cum += decile_event

        decile_count_cum += decile_count

        print(decile_n + 1, decile_event_cum / decile_count_cum / overall_rate)
        
def profile(fit, x_test, rank_count = 10):
    # Decile profile for overall
    scores = fit.predict(x_test)
    rank = (pd.DataFrame(scores, columns = ['rank']).rank() * rank_count // len(scores))
    rank['rank'][rank['rank'] == rank_count] = rank_count-1
    scored = pd.concat([x_test, rank], axis = 1)

    decile_profile = scored.groupby('rank').mean()
    
    return decile_profile

################## OTHER MISCELLANEOUS FUNCTIONS#############################
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
    
    print(pd.concat([foo, bar], axis = 0))
    
def proc_means(df, Class, Val):
    total_count = df.shape[0]
    total_sum = df[Val].sum()
    total_mean = df[Val].mean()
    count = df.groupby(Class)[Val].count()
    Sum = df.groupby(Class)[Val].sum()
    Mean = df.groupby(Class)[Val].mean()
    foo = pd.concat([count.rename("Count"), Sum.rename("Sum"), Mean.rename("Mean")], axis = 1)
    bar = pd.DataFrame([[total_count, total_sum, total_mean]], columns = ['Count', 'Sum', 'Mean'], index = ['Total'])
    
    print(pd.concat([foo, bar], axis = 0))
