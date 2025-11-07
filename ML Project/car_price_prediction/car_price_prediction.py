# car_price_prediction.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
print("Loading dataset...")
url = "https://raw.githubusercontent.com/amankharwal/Website-data/master/Car%20details%20v3.csv"
data = pd.read_csv(url)

# Display first few rows
print("Dataset Loaded Successfully!\n")
print(data.head())

# Check for missing values
print("\nMissing values per column:\n", data.isnull().sum())

# Drop nulls if any
data.dropna(inplace=True)

# Select features and target
X = data[['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner']]
y = data['selling_price']

# Encode categorical variables
le = LabelEncoder()
for col in ['fuel', 'seller_type', 'transmission', 'owner']:
    X[col] = le.fit_transform(X[col])

# Split data into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)

# Train Random Forest model
rf = RandomForestRegressor(random_state=42, n_estimators=100)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

# Evaluate both models
print("\nModel Evaluation Results:")
print("-" * 30)
print(f"Linear Regression R² Score: {r2_score(y_test, lr_preds):.2f}")
print(f"Random Forest R² Score: {r2_score(y_test, rf_preds):.2f}")
print(f"Mean Absolute Error (Random Forest): {mean_absolute_error(y_test, rf_preds):.2f}")

# Visualize actual vs predicted prices
plt.figure(figsize=(8,6))
sns.scatterplot(x=y_test, y=rf_preds, color='teal')
plt.xlabel("Actual Selling Price")
plt.ylabel("Predicted Selling Price")
plt.title("Actual vs Predicted Car Prices (Random Forest)")
plt.show()

# Predict for new car input
print("\n--- Predicting New Car Price ---")
new_car = pd.DataFrame({
    'year': [2015],
    'km_driven': [45000],
    'fuel': le.transform(['Petrol']),
    'seller_type': le.transform(['Individual']),
    'transmission': le.transform(['Manual']),
    'owner': le.transform(['First Owner'])
})
predicted_price = rf.predict(new_car)[0]
print(f"Estimated Selling Price: ₹{predicted_price:,.0f}")
