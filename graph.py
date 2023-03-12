import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('look.csv')
new_df = pd.DataFrame(index=df.columns, columns=df.columns)

df = df[df.columns[1:]]
df = df.drop([0])

for col1 in df.columns:
    for col2 in df.columns:
        if col1 != col2:
            temp_df = (df[col1].astype(float) - df[col2].astype(float)) ** 2
            temp_df = temp_df.sum()

            new_df[col1][col2] = temp_df

new_df = new_df[new_df.columns[1:]].fillna(0)
new_df = new_df.iloc[1:, :]
new_df = (new_df - new_df.min()) / (new_df.max() - new_df.min())

new_df = new_df.replace(0, np.nan)
for col in new_df.columns:
    print(col)
    print(new_df.nsmallest(5, col))
"""
G = nx.from_numpy_array(new_df.values)
G = nx.relabel_nodes(G, dict(enumerate(df.columns)))

edges = G.edges()
weights = [ 1.1 * G[u][v]['weight'] for u,v in edges]

plt.figure(figsize=(16,9))

nodelist = df.columns

nx.draw(G, nodelist=nodelist, with_labels=True, width=weights)

plt.show()
"""

