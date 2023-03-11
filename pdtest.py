import pandas as pd

feature_1 = ['Boston', 'Boston', 'Chicago', 'ATX', 'NYC']
feature_2 = ['LA', 'SFO', 'LA', 'ATX', 'NJ']
score = ['1.00', '0.83', '0.34', '0.98', '0.89']

df = pd.DataFrame({'f1': feature_1, 'f2': feature_2, 'score': score})
print(df)

