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
