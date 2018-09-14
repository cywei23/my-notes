
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

