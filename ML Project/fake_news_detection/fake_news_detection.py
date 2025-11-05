# fake_news_detection.py

import pandas as pd
import numpy as np
import re
import string
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -------------------------
# 1️⃣ Load Dataset
# -------------------------
# You can replace this with your own dataset
# Example dataset: https://www.kaggle.com/c/fake-news/data
print("Loading dataset...")
df = pd.read_csv("https://raw.githubusercontent.com/laxmimerit/fake-news-detection/main/fake_or_real_news.csv")

print("Dataset loaded successfully!")
print(df.head())

# -------------------------
# 2️⃣ Data Preprocessing
# -------------------------
print("\nPreprocessing data...")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

df['text'] = df['text'].apply(clean_text)

# -------------------------
# 3️⃣ Feature & Label Split
# -------------------------
X = df['text']
y = df['label']

# -------------------------
# 4️⃣ TF-IDF Vectorization
# -------------------------
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_vect = vectorizer.fit_transform(X)

# -------------------------
# 5️⃣ Train-Test Split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

# -------------------------
# 6️⃣ Model Training
# -------------------------
print("\nTraining model...")
model = LogisticRegression()
model.fit(X_train, y_train)

# -------------------------
# 7️⃣ Evaluation
# -------------------------
print("\nEvaluating model...")
y_pred = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -------------------------
# 8️⃣ Save Model
# -------------------------
joblib.dump(model, "fake_news_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("\n✅ Model and vectorizer saved successfully!")

# -------------------------
# 9️⃣ Prediction Function
# -------------------------
def predict_news(text):
    text = clean_text(text)
    vect_text = vectorizer.transform([text])
    prediction = model.predict(vect_text)
    return prediction[0]

# Example prediction
print("\nExample Test:")
test_news = "Breaking news: The government has announced a new tax policy for 2025."
print(f"Prediction: {predict_news(test_news)}")
