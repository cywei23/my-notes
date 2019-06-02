#### THIS IS JUST PSEUDO CODE!!! ####

# Find out cardinality on all columns and then one-hot encoding
cardinality = [[col, len(df[col].unique())] for col in df.columns]
cardinality = pd.DataFrame(cardinality)
cardinality.columns = 'column card'.split()

column_list_ohe = cardinality[cardinality['card'] <= max_level_to_OHE]
column_list_ohe = column_list_ohe['column'].values.tolist()

# 10 minutes to pandas
df.mean()
df.mean(1)

df.apply(np.cumsum)
df.apply(lambda x: x.max() - x.min())

df.col.str.lower()
df.col.str.contains()

df.describe(include = ['O']) # non-numeric columns only
df.describe(include = 'all') # all columns

# Frequency Analysis
df.col.value_counts(normalize=True, dropna=False)
df.col.value_counts(bins=10).sort_index(ascending=False)
# custom range
df = pd.DataFrame({"a": np.random.random_integers(0, high=100, size=100)})
ranges = [0,10,20,30,40,50,60,70,80,90,100]
df.groupby(pd.cut(df.a, ranges)).count()

# Define my own range - interval_range
intervals = pd.interval_range(start=0, end=600, freq=60)
gr_freq_table_10 = pd.Series([0 for x in range(10)], index=intervals)
for i in wnba['PTS']:
    for j in intervals:
        if i in j:
            gr_freq_table_10.loc[j] += 1

# map method with dictionary to change value
mapping_dict = {
    'Android': 'Android',
    'Chrome OS': 'Chrome OS',
    'Linux': 'Linux',
    'Mac OS': 'macOS',
    'No OS': 'No OS',
    'Windows': 'Windows',
    'macOS': 'macOS'
}
laptops['os'] = laptops['os'].map(mapping_dict)

# cleaning data with str.split(n=1, expand=True), strip() to get rid of leading and trailing space
for i in ['storage_1','storage_2']:
    s_capacity = i+'_capacity_gb'
    s_type = i+'_type'
    laptops[[s_capacity,s_type]]=laptops[i].str.split(n=1,expand=True)
    laptops[s_capacity]=laptops[s_capacity].astype(float)
    laptops[s_type]=laptops[s_type].str.strip()
laptops.drop(['storage','storage_1','storage_2'],axis=1,inplace=True)

# rename column
laptops.rename({"screen_size": "screen_size_inches"}, axis=1, inplace=True)

# use function and list comprehension to clean column names
def clean_col(s):
    s = s.strip()
    s = s.replace('Operating System','os')
    s = s.replace(' ','_')
    s = s.replace('(','')
    s = s.replace(')','')
    s = s.lower()
    return s    
laptops.columns = [clean_col(i) for i in laptops.columns]

# this is the way to put Series into Dictionary
dtypes = optimized_gl.drop('date',axis=1).dtypes
dtypes_col = dtypes.index
dtypes_type = [i.name for i in dtypes.values]
column_types = dict(zip(dtypes_col, dtypes_type))

# prettyprinter for dictionary
import pprint
pp = pprint.PrettyPrinter()
pp.pprint(column_types)

# list permutation
import itertools
perm = list(itertools.permutations(hundreds_col, 2))
