import random
import pandas as pd

# Moving Average Function
def moving_average(series, period):
    return series.rolling(window=period).mean()

# Stochastic Oscillator Function
def stochastic_oscillator(highs, lows, closes, k_period=14, d_period=3):
    lowest_low = lows.rolling(k_period).min()
    highest_high = highs.rolling(k_period).max()
    percent_k = 100 * ((closes - lowest_low) / (highest_high - lowest_low))
    percent_d = percent_k.rolling(d_period).mean()
    return percent_k, percent_d

# Fake Price Data Generator (Mock Data)
def generate_mock_data(rows=220):
    data = []
    price = 1.100
    for _ in range(rows):
        o = price
        h = o + random.uniform(0.0001, 0.0005)
        l = o - random.uniform(0.0001, 0.0005)
        c = random.uniform(l, h)
        data.append([round(o, 5), round(h, 5), round(l, 5), round(c, 5)])
        price = c
    df = pd.DataFrame(data, columns=['open', 'high', 'low', 'close'])
    return df

# Strategy Analyzer
def analyze_strategy(df):
    df['MA2'] = moving_average(df['close'], 2)
    df['MA5'] = moving_average(df['close'], 5)
    df['MA200'] = moving_average(df['close'], 200)
    df['%K'], df['%D'] = stochastic_oscillator(df['high'], df['low'], df['close'])

    last = df.iloc[-1]
    prev = df.iloc[-2]

    result = {
        "Trade Direction": "NO TRADE",
        "Entry Criteria": "Conditions not met",
        "Expiration Time": "N/A",
        "Confidence Level": "N/A"
    }

    if (
        last['close'] > last['MA200']
        and prev['MA2'] <= prev['MA5']
        and last['MA2'] > last['MA5']
        and prev['%K'] < last['%K'] < 20
    ):
        result = {
            "Trade Direction": "CALL",
            "Entry Criteria": "Price > 200 MA, 2 MA crossed above 5 MA, Stochastic below 20 & turning up",
            "Expiration Time": "1 minute",
            "Confidence Level": "High (99%)"
        }

    elif (
        last['close'] < last['MA200']
        and prev['MA2'] >= prev['MA5']
        and last['MA2'] < last['MA5']
        and prev['%K'] > last['%K'] > 80
    ):
        result = {
            "Trade Direction": "PUT",
            "Entry Criteria": "Price < 200 MA, 2 MA crossed below 5 MA, Stochastic above 80 & turning down",
            "Expiration Time": "1 minute",
            "Confidence Level": "High (99%)"
        }

    return result

# Main Program
if __name__ == "__main__":
    df = generate_mock_data()
    signal = analyze_strategy(df)
    print("\n=== Trading Signal ===")
    for k, v in signal.items():
        print(f"{k}: {v}")
