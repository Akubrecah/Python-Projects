import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings

warnings.filterwarnings("ignore")

# Configuration
SYMBOL = 'AAPL'
START_DATE = '2020-01-01'
END_DATE = '2023-01-01'
BUFFER = 0.002  # Buffer percentage for advanced strategy
SHORT_WINDOW = 20
MEDIUM_WINDOW = 50
LONG_WINDOW = 200

def fetch_stock_data(symbol, start, end):
    """Retrieve historical stock data"""
    return yf.download(symbol, start=start, end=end)

def calculate_technical_indicators(data):
    """Compute technical indicators and trading signals"""
    # Calculate moving averages
    data['SMA_20'] = data['Close'].rolling(SHORT_WINDOW).mean()
    data['SMA_50'] = data['Close'].rolling(MEDIUM_WINDOW).mean()
    data['SMA_200'] = data['Close'].rolling(LONG_WINDOW).mean()
    
    # Generate signals
    data = _generate_simple_signals(data)
    data = _generate_advanced_signals(data, BUFFER)
    
    return data.dropna()

def _generate_simple_signals(data):
    """Simple SMA crossover strategy"""
    data['Signal_Simple'] = np.where(data['SMA_20'] > data['SMA_50'], 1, 0)
    return data

def _generate_advanced_signals(data, buffer):
    """Advanced SMA crossover strategy with buffer zone"""
    # Calculate difference between SMAs
    data['SMA_Diff'] = data['SMA_50'] - data['SMA_200']
    data['Prev_SMA_Diff'] = data['SMA_Diff'].shift(1)
    
    # Initialize signals and events
    data['Signal_Advanced'] = 0
    data['Event'] = np.nan
    
    # Identify signal events
    golden_cross = (data['Prev_SMA_Diff'] < -buffer) & (data['SMA_Diff'] > buffer)
    death_cross = (data['Prev_SMA_Diff'] > buffer) & (data['SMA_Diff'] < -buffer)
    buffer_zone = data['SMA_Diff'].abs() <= buffer
    
    # Apply signals
    data.loc[golden_cross, 'Signal_Advanced'] = 1
    data.loc[death_cross, 'Signal_Advanced'] = -1
    data.loc[buffer_zone, 'Event'] = 'Buffer Zone'
    
    # Propagate signals forward
    data['Signal_Advanced'] = data['Signal_Advanced'].replace(0, np.nan).ffill().fillna(0)
    
    # Mark events
    data.loc[golden_cross, 'Event'] = 'Golden Cross'
    data.loc[death_cross, 'Event'] = 'Death Cross'
    
    # Cleanup temporary columns
    return data.drop(columns=['SMA_Diff', 'Prev_SMA_Diff'])

def prepare_training_data(data, signal_type='Simple'):
    """Prepare features and target for model training"""
    feature_cols = ['SMA_20', 'SMA_50', 'SMA_200']
    target_col = f'Signal_{signal_type}'
    
    X = data[feature_cols]
    y = data[target_col]
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_random_forest(X_train, y_train):
    """Train Random Forest classifier"""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    # Visualize confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Sell', 'Buy'] if y_test.nunique() == 2 else ['Sell', 'Hold', 'Buy'],
                yticklabels=['Sell', 'Buy'] if y_test.nunique() == 2 else ['Sell', 'Hold', 'Buy'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

def visualize_strategy(data, strategy_type='Simple'):
    """Visualize trading strategy"""
    plt.figure(figsize=(14, 7))
    
    # Plot price and SMAs
    plt.plot(data['Close'], label='Close Price', alpha=0.7)
    plt.plot(data['SMA_20'], label='20-Day SMA', alpha=0.7)
    plt.plot(data['SMA_50'], label='50-Day SMA', alpha=0.7)
    plt.plot(data['SMA_200'], label='200-Day SMA', alpha=0.7)
    
    # Plot signals based on strategy type
    signal_col = f'Signal_{strategy_type}'
    if strategy_type == 'Simple':
        buy_signals = data[data[signal_col] == 1]
        plt.scatter(buy_signals.index, buy_signals['Close'], 
                    marker='^', color='green', s=100, label='Buy Signal')
    else:
        buy_signals = data[data[signal_col] == 1]
        sell_signals = data[data[signal_col] == -1]
        plt.scatter(buy_signals.index, buy_signals['Close'], 
                    marker='^', color='green', s=100, label='Buy Signal')
        plt.scatter(sell_signals.index, sell_signals['Close'], 
                    marker='v', color='red', s=100, label='Sell Signal')
        
        # Mark special events
        events = data.dropna(subset=['Event'])
        for event_type, marker, color in [('Golden Cross', '*', 'gold'), 
                                        ('Death Cross', 'X', 'black'), 
                                        ('Buffer Zone', 'o', 'blue')]:
            event_data = events[events['Event'] == event_type]
            plt.scatter(event_data.index, event_data['Close'], 
                        marker=marker, color=color, s=150, label=event_type)
    
    plt.title(f'{SYMBOL} Price and {strategy_type} Strategy Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

def main():
    """Main execution function"""
    # Data acquisition and processing
    stock_data = fetch_stock_data(SYMBOL, START_DATE, END_DATE)
    stock_data = calculate_technical_indicators(stock_data)
    
    # Model training and evaluation for simple strategy
    X_train, X_test, y_train, y_test = prepare_training_data(stock_data, 'Simple')
    model = train_random_forest(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    
    # Visualization
    visualize_strategy(stock_data, 'Simple')
    visualize_strategy(stock_data, 'Advanced')
    
    # Advanced strategy insights
    print("\nAdvanced Strategy Events:")
    print(stock_data['Event'].value_counts(dropna=False))
    
    print("\nSignal Change Points:")
    changes = stock_data[stock_data['Signal_Advanced'].diff() != 0]
    print(changes[['Close', 'SMA_50', 'SMA_200', 'Signal_Advanced', 'Event']].head())

if __name__ == "__main__":
    main()