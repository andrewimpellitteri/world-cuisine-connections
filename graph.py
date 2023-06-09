import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import jaccard
from scipy.stats.stats import pearsonr   


df = pd.read_csv('look_edit2.csv')
pop_weights = pd.read_csv('pop_weights.csv').to_dict()


cleaned = []
for v in pop_weights.values():
    cleaned.append(v.values())

pop_weights = dict(zip(cleaned[0], cleaned[1]))



df = df[df.columns[1:]]
df = df.drop([0])

def calc_sim(df):

    new_df = pd.DataFrame(index=df.columns, columns=df.columns)

    for col1 in df.columns:
        for col2 in df.columns:
            if col1 != col2:
                # euclidean distance
                # temp_df = (df[col1].astype(float) - df[col2].astype(float)) ** 2
                # temp_df = temp_df.sum()
                c1 = np.nan_to_num(df[col1].astype(float).values.reshape(1,-1))
                c2 = np.nan_to_num(df[col2].astype(float).values.reshape(1,-1))
                
                c1 /= pop_weights[col1] 
                c2 /= pop_weights[col2]

                print(c1)

                # temp_df = cosine_similarity(c1, c2)
                
                jac = jaccard(c1[0], c2[0])
                
                temp_df =  (1 + pearsonr(c1[0], c2[0])[0]) * jac

                print(temp_df)
                new_df[col1][col2] = temp_df

    new_df = new_df[new_df.columns[1:]].fillna(0)
    new_df = new_df.iloc[1:, :]
    new_df = (new_df - new_df.min()) / (new_df.max() - new_df.min())

    return new_df


new_df = calc_sim(df)
# new_df = 1 - new_df

plt.hist(new_df)
plt.show()

closest = {}
for col in new_df.columns:
    so = list(new_df[col].astype(float).fillna(0).sort_values(ascending=False).index[1:10])
    so = [e.strip(' ') for e in so]

    closest[col] = so

print(list(closest.values()), sep="\n")
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


def weighting_fn(w, cutoff, src):
    
    if w < cutoff:
        return 0
    try:
        reweight = pop_weights[src]
        w /= reweight ** 3
    except KeyError as e:
        # print(e)
        pass
    # inv = 1 - w
    # sig = 1/(1 + np.exp(-inv))
    
    return 5 * w

def html_network(df):

    got_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # got_net.show_buttons(filter_=['physics'])

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
                    w = weighting_fn(e[2], cutoff=0.001, src=e[0])
                    
                    got_net.add_node(src, src, title=src)
                    got_net.add_node(dst, dst, title=dst)
                    if src != dst:
                        got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    # add neighbor data to node hover data
    for node in got_net.nodes:
                    node["title"] += " Closest Neighbors: " + " ".join(closest[node["id"]])
                    node["value"] = len(closest[node["id"]])

    got_net.show("connection_map.html")

html_network(new_df)