import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network

df = pd.read_csv('look_bert2.csv')
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
"""
mean_df = new_df.mean(axis=0).sort_values()
print(mean_df)

plt.imshow(new_df)

plt.colorbar()
  
# Assigning labels of x-axis 
# according to dataframe
plt.xticks(range(len(new_df)), new_df.columns, rotation=45)
  
# Assigning labels of y-axis 
# according to dataframe
plt.yticks(range(len(new_df)), new_df.index)
  
# Displaying the figure
plt.show()

new_df = new_df.replace(0, np.nan)
for col in new_df.columns:
    print(col)
    print(new_df.nsmallest(5, col))


G = nx.from_numpy_array(new_df.values)
G = nx.relabel_nodes(G, dict(enumerate(df.columns)))

edges = G.edges()
weights = [weighting_fn(G[u][v]['weight']) for u,v in edges]

plt.figure(figsize=(16,9))

nodelist = df.columns

nx.draw(G, nodelist=nodelist, with_labels=True, width=weights)

plt.show()
"""


def weighting_fn(w):
    # inv = 1 - w
    # sig = 1/(1 + np.exp(-inv))
    return (1 - w) ** 15

def html_network(df):

    got_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", select_menu=True)

    got_net.show_buttons(filter_=['physics'])

    # set the physics layout of the network
    got_net.barnes_hut()


    stacked_df = df.stack().reset_index()

    # Rename the columns
    stacked_df.columns = ['row', 'column', 'value']

    # Convert to a list of tuples
    edge_data = list(stacked_df.itertuples(index=False, name=None))
    
    
    for e in edge_data:
                    src = e[0]
                    dst = e[1]
                    w = weighting_fn(e[2])

                    got_net.add_node(src, src, title=src)
                    got_net.add_node(dst, dst, title=dst)
                    got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    # add neighbor data to node hover data
    for node in got_net.nodes:
                    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
                    node["value"] = len(neighbor_map[node["id"]])

    got_net.show("connection_map.html")

html_network(new_df)