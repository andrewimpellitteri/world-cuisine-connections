import pandas as pd

df_bert = pd.read_csv("look_bert.csv")
df_TFIDF = pd.read_csv("look_TFIDF.csv")
df_base = pd.read_csv("look.csv")

models = [df_base, df_bert, df_TFIDF]


for model in models:
    print(model)