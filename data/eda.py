import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset and remove the first two rows
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

# Drop rows with missing values in critical columns
df.dropna(subset=['date', 'item_name', 'value'], inplace=True)

# Verify data types
print("\nData Types After Cleaning:")
print(df.dtypes)

# Ensure no negative prices
df = df[df['value'] >= 0]

# Filter data for specific item types and plot their price over time
item_names = df['item_name'].unique()

for item in item_names:
    plt.figure(figsize=(15, 10))
    item_data = df[df['item_name'] == item]
    sns.lineplot(data=item_data, x='date', y='value')
    plt.title(f'Price Trends Over Time for {item}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(title='Item Name')
    plt.show()

# Line charts to analyze impact of significant events
events = {
    'Election 2007': '2007-12-27',
    'Post-election violence 2007': '2007-12-30',
    'Election 2013': '2013-03-04',
    'Election 2017': '2017-08-08'
}

for item in item_names:
    plt.figure(figsize=(15, 10))
    item_data = df[df['item_name'] == item]
    sns.lineplot(data=item_data, x='date', y='value')
    for event, date in events.items():
        plt.axvline(pd.to_datetime(date), color='red', linestyle='--', lw=2, label=event)
    plt.title(f'Impact of Events on {item} Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(title='Event')
    plt.show()

# Overall price trends for all items
plt.figure(figsize=(15, 10))
sns.lineplot(data=df, x='date', y='value', hue='item_name')
plt.title('Overall Price Trends for All Items Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(title='Item Name')
plt.show()

print("EDA Completed. Please refer to the plots for insights.")
