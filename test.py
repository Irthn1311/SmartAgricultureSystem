import pandas as pd

df = pd.read_csv("Weather_Data.csv")
print(df["RainTomorrow"].value_counts())
