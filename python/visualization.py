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
