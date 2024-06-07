import pandas as pd

df = pd.read_excel("/home/sr9000/Downloads/Арсенал.xlsx")

print(df)

print(df.info())

print(list(df.itertuples(index=False, name=None)))
