# predictor/views.py

import pandas as pd
import joblib
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Load the data into a DataFrame
df = pd.read_csv('model/wfp_food_prices_ken.csv')

# List all columns required by the model
required_columns = [
    'adm1_name', 'adm2_name', 'loc_market_name', 'item_type',
    'item_name', 'item_unit', 'item_price_type', 'currency',
    'value', 'year', 'month', 'day'
]

df = df[required_columns]

# Load the pre-trained model
model = joblib.load('model/data/price_prediction_model.pkl')

def preprocess_input(data):
    # Convert input data to DataFrame
    input_df = pd.DataFrame([data])
    
    # Add default values for the necessary columns that the user does not input
    input_df['adm1_name'] = 'Unknown'
    input_df['adm2_name'] = 'Unknown'
    input_df['item_type'] = 'Unknown'
    input_df['item_unit'] = 'KG'  # or any default value that makes sense
    input_df['item_price_type'] = 'Unknown'
    input_df['currency'] = 'KES'  # or any default value that makes sense
    input_df['value'] = 0.0  # Default or calculated value
    
    input_df = input_df[['year', 'month', 'day', 'item_name', 'loc_market_name', 
                         'adm1_name', 'adm2_name', 'item_type', 'item_unit', 'item_price_type', 'currency', 'value']]
    return input_df

@csrf_exempt
def predict_price(request):
    if request.method == 'POST':
        date_parts = request.POST.get('date').split('-')
        data = {
            'year': int(date_parts[0]),
            'month': int(date_parts[1]),
            'day': int(date_parts[2]),
            'item_name': request.POST.get('item_name'),
            'loc_market_name': request.POST.get('loc_market_name')
        }
        print(f"Received data: {data}")  # Debugging line
        try:
            input_df = preprocess_input(data)
            print(f"Preprocessed input: {input_df}")  # Debugging line
            predicted_price = model.predict(input_df)[0]
            response = {
                'predicted_price': predicted_price
            }
            print(f"Prediction response: {response}")  # Debugging line
        except Exception as e:
            response = {
                'error': str(e)
            }
            print(f"Error response: {response}")  # Debugging line
        return JsonResponse(response)
    else:
        context = {
            'items': df['item_name'].unique(),
            'locations': df['loc_market_name'].unique()
        }
        return render(request, 'predictor/index.html', context)

def show_analytics(request):
    return render(request, 'predictor/analytics.html')

def get_analytics(request):
    # Fetch price trend data from the dataframe
    trend_data = df.groupby('date')['value'].mean().reset_index()
    trend_data['date'] = trend_data['date'].dt.strftime('%Y-%m-%d')

    data = {
        'dates': trend_data['date'].tolist(),
        'prices': trend_data['value'].tolist(),
    }
    return JsonResponse(data)
