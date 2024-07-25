import pandas as pd

# Load the dataset
file_path = 'wfp_food_prices_ken.csv'
df = pd.read_csv(file_path, skiprows=2, header=None)

# Manually specify the column names
df.columns = [
    'date', 'adm1_name', 'adm2_name', 'loc_market_name', 'geo_lat', 'geo_lon', 
    'item_type', 'item_name', 'item_unit', 'item_price_flag', 'item_price_type', 
    'currency', 'value', 'value_usd'
]

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Drop unnecessary columns
df = df.drop(columns=['geo_lat', 'geo_lon', 'item_price_flag'])

# Extract year, month, and day as separate features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

# Drop rows with missing values in critical columns
df.dropna(subset=['date', 'item_name', 'value'], inplace=True)

# Drop the original 'date' column
df.drop(columns=['date'], inplace=True)

# Save the cleaned dataset
df.to_csv('wfp_food_prices_ken.csv', index=False)
