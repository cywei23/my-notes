import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# adjust matplotlib default figure size
plt.rcParams['figure.figsize'] = [14, 4]

# Compare distribution between groups
cols = ['highcredit','balance','creditlimit']
for i in cols:
    # can add row and col for additional groups to bread down
    g = sns.FacetGrid(dftr[dftr[i]<100000], hue='bureau', size=5)
    g.map(sns.distplot, i, hist=False)
    g.add_legend()
    g.fig.suptitle(i)
    plt.show()

# Heatmap for comparing model decile distribution
## create list combination first
import itertools
perm = list(itertools.combinations(hundreds_col, 2))

## create heatmap
for i in perm:
    bnsr_gb = bnsr.groupby(list(i), as_index=False).agg({'consumer_id':'count'})
    bnsr_gb['consumer_id'] = bnsr_gb['consumer_id']/488862*100
    bnsr_gb = bnsr_gb.pivot(list(i)[0], list(i)[1], 'consumer_id')
    ax = sns.heatmap(bnsr_gb, annot=True, fmt='.1f', cmap="YlGnBu")
    ax.invert_yaxis()
    plt.show()

## quickly create histogram
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
pd.read_sql_query(q4, conn).hist(ax=ax)

## pie chart
wnba['Exp_ordinal'].value_counts().plot.pie(figsize = (6,6), autopct = '%.2f%%',
                                    title = 'Percentage of players in WNBA by level of experience')
plt.ylabel('')

## Data prep for Violin Chart, using set_index and stack data
# keep the column we need, index1 = ownership, index2 = co_focus_flg, socres = value columns
df4 = df[['ownership', 'co_focus_flg'] + scores].copy()
# transform column to be readable for charting
df4['co_focus_flg'] = np.where(df4['co_focus_flg']==1, 'Focus Owner', 'Non Focus Owner')
# set_index for stacking the data
df4.set_index(['ownership', 'co_focus_flg'], inplace=True)
print(df4.head())
# stacking data
stacked = df4.stack().reset_index()
print(stacked.shape)
# rename columns for charting
stacked = stacked.rename({'level_2':'Propensity Model', 0: 'Rank'}, axis=1)
print(stacked.head())
