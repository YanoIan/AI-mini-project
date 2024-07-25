from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import pandas as pd

# Load the cleaned dataset

df = pd.read_csv('wfp_food_prices_ken.csv') 
# Define feature columns and target column
feature_cols = ['adm1_name', 'adm2_name', 'loc_market_name', 
                'item_type', 'item_name', 'item_unit', 
                'item_price_type', 'currency', 'year', 'month', 'day']
target_col = 'value'

# Split the data into features and target
X = df[feature_cols]

























































































































































































































































































































y = df[target_col]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess the data
numeric_features = ['year', 'month', 'day']
categorical_features = ['adm1_name', 'adm2_name', 'loc_market_name', 'item_type', 
                        'item_name', 'item_unit', 'item_price_type', 'currency']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Create the model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'data/price_prediction_model.pkl')

# Print model evaluation metrics
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Model Evaluation:\nMSE: {mse}\nR2 Score: {r2}')
