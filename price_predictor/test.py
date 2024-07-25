import pandas as pd

# Load the dataset
df = pd.read_csv('model/wfp_food_prices_ken.csv')

# Display the first few rows and the columns
print(df.head())
print(df.columns)
