# stock_lstm.py
"""
Stock Price Prediction using LSTM

Usage:
    python stock_lstm.py --ticker AAPL --period 5y --lookback 60 --epochs 20 --batch 32

This script:
- downloads historical 'Close' price data using yfinance
- scales data with MinMaxScaler
- creates time-series sequences (X) and labels (y)
- builds and trains an LSTM model (Keras)
- evaluates model (RMSE) and plots predictions vs actual
- saves trained model and scaler to disk
"""

import argparse
import os
import random
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

# --------------------
# Reproducibility
# --------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# --------------------
# Helpers
# --------------------
def download_data(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
    """
    Download historical data using yfinance.
    Returns DataFrame with Date index and columns (Open, High, Low, Close, Adj Close, Volume)
    """
    print(f"[{datetime.now()}] Downloading {ticker} data for period={period}, interval={interval} ...")
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df.empty:
        raise ValueError("No data downloaded — check ticker symbol or internet connection.")
    df = df[['Close']].copy()
    df.dropna(inplace=True)
    return df

def create_sequences(values: np.ndarray, look_back: int):
    """
    Create sequences of length `look_back` for LSTM input.
    X shape: (num_samples, look_back, 1)
    y shape: (num_samples,)
    """
    X, y = [], []
    for i in range(look_back, len(values)):
        X.append(values[i - look_back:i, 0])
        y.append(values[i, 0])
    X = np.array(X)
    y = np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    return X, y

def build_model(input_shape, units=50, dropout=0.2):
    model = Sequential()
    model.add(LSTM(units=units, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(dropout))
    model.add(LSTM(units=units // 2, return_sequences=False))
    model.add(Dropout(dropout))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# --------------------
# Main Pipeline
# --------------------
def run(ticker: str, period: str, look_back: int, epochs: int, batch: int, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # 1) Download
    df = download_data(ticker, period=period)
    print(f"Downloaded {len(df)} rows. Sample:")
    print(df.tail(3))

    # 2) Scale
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(df.values)  # shape (n_rows, 1)

    # Save scaler for later (so predictions on new data use same transform)
    import joblib
    scaler_path = os.path.join(output_dir, f"{ticker}_scaler.save")
    joblib.dump(scaler, scaler_path)
    print(f"Saved scaler to {scaler_path}")

    # 3) Create sequences
    X, y = create_sequences(scaled, look_back=look_back)

    # 4) Train/Test split (by time — no shuffling)
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

    # 5) Build model
    model = build_model(input_shape=(look_back, 1), units=64, dropout=0.2)
    model.summary()

    # 6) Train
    model_path = os.path.join(output_dir, f"{ticker}_lstm_best.h5")
    checkpoint = ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1)
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch,
        validation_data=(X_test, y_test),
        callbacks=[checkpoint],
        verbose=2
    )

    # load best model
    model.load_weights(model_path)
    final_model_path = os.path.join(output_dir, f"{ticker}_lstm_final.h5")
    model.save(final_model_path)
    print(f"Saved final model to {final_model_path}")

    # 7) Predict
    y_pred_scaled = model.predict(X_test)
    # inverse scale
    y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))
    y_pred_inv = scaler.inverse_transform(y_pred_scaled)

    # 8) Evaluate
    rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
    print(f"Test RMSE: {rmse:.4f}")

    # 9) Plot actual vs predicted (aligned to dates)
    test_dates = df.index[look_back + split: look_back + split + len(y_test)]
    plt.figure(figsize=(12, 6))
    plt.plot(test_dates, y_test_inv, label='Actual Price')
    plt.plot(test_dates, y_pred_inv, label='Predicted Price')
    plt.title(f"{ticker} — Actual vs Predicted (Test set)")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plot_path = os.path.join(output_dir, f"{ticker}_prediction_plot.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.show()
    print(f"Saved plot to {plot_path}")

    # 10) Optionally: Predict next day using the last `look_back` values
    last_sequence = scaled[-look_back:].reshape(1, look_back, 1)
    next_pred_scaled = model.predict(last_sequence)
    next_pred = scaler.inverse_transform(next_pred_scaled)[0, 0]
    last_date = df.index[-1].strftime("%Y-%m-%d")
    print(f"Last available date: {last_date}")
    print(f"Predicted next close price for {ticker}: {next_pred:.4f}")

    return {
        "model_path": final_model_path,
        "scaler_path": scaler_path,
        "plot_path": plot_path,
        "rmse": rmse,
        "next_pred": float(next_pred),
    }

# --------------------
# CLI
# --------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Price Prediction using LSTM")
    parser.add_argument("--ticker", type=str, required=True, help="Ticker symbol (e.g., AAPL)")
    parser.add_argument("--period", type=str, default="5y", help="History period for yfinance (e.g., 1y, 5y, max)")
    parser.add_argument("--lookback", type=int, default=60, help="Number of days in input sequences")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=32, help="Training batch size")
    parser.add_argument("--output", type=str, default="output", help="Folder to save model & plots")
    args = parser.parse_args()

    results = run(args.ticker.upper(), args.period, args.lookback, args.epochs, args.batch, args.output)
    print("\nDone. Results summary:")
    for k, v in results.items():
        print(f" - {k}: {v}")
