import pandas as pd
import numpy as np
from polyfuzz import PolyFuzz
from polyfuzz.models import Embeddings
from flair.embeddings import TransformerWordEmbeddings
from tqdm import tqdm

embeddings = TransformerWordEmbeddings('bert-base-multilingual-cased')
bert = Embeddings(embeddings, min_similarity=0, model_id="BERT")

df = pd.read_csv('testBig.csv')

# TODO: #1 rescrape allrecipes to get the number recipies in each cusine
# then divide the values in each to scale


first = df.columns[1]
all_d = []
for col in df.columns:
    for v in df[col].values:
        if isinstance(v, str):
            all_d.append(v)



model = PolyFuzz(bert)
tqdm(model.match(all_d, all_d))
model.group(link_min_similarity=0.50)
model.get_matches()
cluster_dict = model.get_clusters()

cluster_dict = {k: sorted(v, key=len) for (k, v) in cluster_dict.items()}

replace_dict = {}

for idx, cluster in cluster_dict.items():
    shortest = cluster[0]
    print(shortest)
    print(cluster[1:])
    for ele in cluster:
        replace_dict[ele] = shortest


df.replace(to_replace=replace_dict, inplace=True)

df = df[df.columns[1:]]

to_concat = []

for col in df.columns:
    summ = df.groupby(col).agg(['count'])
    to_concat.append(summ)

df = pd.concat(to_concat)
df.to_csv('look_bert2.csv')
print(df)

