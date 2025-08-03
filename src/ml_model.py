# src/ml_model.py
import numpy as np  # <-- FIX: Import numpy
from sklearn.model_selection import train_test_split
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas_ta as ta
import logging

def get_ml_prediction(df):
    
    # 1. Feature Engineering
    df.ta.macd(append=True)
    df.ta.rsi(append=True)
    df['Volume_Change'] = df['Volume'].pct_change()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # --- FIX: Replace infinite values with NaN ---
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    # --- End of FIX ---

    df.dropna(inplace=True)
    
    features = ['RSI_14', 'MACD_12_26_9', 'Volume_Change']
    X = df[features]
    y = df['Target']
    
    if len(df) < 20:
        logging.warning("Not enough data for ML prediction.")
        return "N/A", 0

    # 2. Model Training & Evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    #model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    
    # 3. Predict for tomorrow
    prediction = model.predict(df[features].iloc[[-1]])[0]
    prediction_label = "UP" if prediction == 1 else "DOWN"
    
    logging.info(f"ML Model Accuracy: {accuracy:.2f}, Prediction: {prediction_label}")
    return prediction_label, accuracy


