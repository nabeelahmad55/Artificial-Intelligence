# diabetes_prediction.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load Dataset
print("Loading dataset...")
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
data = pd.read_csv(url)
print("Dataset loaded successfully!\n")

print(data.head())

# Check for missing values
print("\nMissing Values:\n", data.isnull().sum())

# Features and target
X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Logistic Regression
lr = LogisticRegression()
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)

# Train Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

# Evaluate models
print("\n--- Model Evaluation ---")
print(f"Logistic Regression Accuracy: {accuracy_score(y_test, lr_preds):.2f}")
print(f"Random Forest Accuracy: {accuracy_score(y_test, rf_preds):.2f}")

# Confusion Matrix
plt.figure(figsize=(6,4))
sns.heatmap(confusion_matrix(y_test, rf_preds), annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix - Random Forest")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Classification Report
print("\nClassification Report:\n", classification_report(y_test, rf_preds))

# Predict for new input
print("\n--- New Patient Prediction ---")
new_data = np.array([[2, 120, 70, 20, 80, 25.5, 0.35, 35]])  # sample input
new_scaled = scaler.transform(new_data)
prediction = rf.predict(new_scaled)

if prediction[0] == 1:
    print("🩸 The patient is likely to have Diabetes.")
else:
    print("✅ The patient is not likely to have Diabetes.")
