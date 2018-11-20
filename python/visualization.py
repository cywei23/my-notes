import matplotlib.pyplot as plt
import seaborn as sns

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
## create list permutation first
import itertools
perm = list(itertools.permutations(hundreds_col, 2))

## create heatmap
for i in perm:
    bnsr_gb = bnsr.groupby(list(i), as_index=False).agg({'consumer_id':'count'})
    bnsr_gb['consumer_id'] = bnsr_gb['consumer_id']/488862*100
    bnsr_gb = bnsr_gb.pivot(list(i)[0], list(i)[1], 'consumer_id')
    ax = sns.heatmap(bnsr_gb, annot=True, fmt='.1f', cmap="YlGnBu")
    ax.invert_yaxis()
    plt.show()

