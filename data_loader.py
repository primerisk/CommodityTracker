import yfinance as yf
import pandas as pd

# Mapping of metal names to Yahoo Finance tickers
# GC=F: Gold
# SI=F: Silver
# PL=F: Platinum
# PA=F: Palladium
# TICKERS Mapping
TICKERS = {
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'Platinum': 'PL=F',
    'Palladium': 'PA=F',
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD'
}

def get_metal_data(symbol_key, period="5y"):
    """
    Fetches historical data for a given metal.
    
    Args:
        symbol_key (str): Key from METAL_TICKERS (e.g., 'Gold').
        period (str): Data period to fetch (e.g., '1mo', '1y', '5y', 'max').
        
    Returns:
        pd.DataFrame: DataFrame with Date index and Close price.
    """
    ticker = TICKERS.get(symbol_key)
    if not ticker:
        return None
    
    # Fetch data
    df = yf.Ticker(ticker).history(period=period)
    
    if df.empty:
        return pd.DataFrame()

    # Clean up DataFrame
    df = df[['Close']]
    df.columns = [symbol_key]
    df.index = df.index.tz_localize(None) # Remove timezone for easier plotting/merging
    return df

def get_current_price(symbol_key):
    """
    Fetches the latest available price for a given metal.
    """
    ticker = TICKERS.get(symbol_key)
    if not ticker:
        return None
        
    t = yf.Ticker(ticker)
    
    # Try fast info first (often more up to date for current price)
    try:
        price = t.fast_info['last_price']
        if price:
            return price
    except:
        pass
        
    # Fallback to history
    df = t.history(period="1d")
    if not df.empty:
        return df['Close'].iloc[-1]
    
    return 0.0

def get_ticker_metrics(symbol_key):
    """
    Fetches the latest price, change, and percent change.
    Returns: (price, change, pct_change)
    """
    ticker = TICKERS.get(symbol_key)
    if not ticker:
        return 0.0, 0.0, 0.0
        
    t = yf.Ticker(ticker)
    
    try:
        current = t.fast_info['last_price']
        prev = t.fast_info['previous_close']
        
        if current and prev:
            change = current - prev
            pct_change = (change / prev) * 100
            return current, change, pct_change
    except:
        pass
        
    # Fallback to history
    try:
        df = t.history(period="5d")
        if len(df) >= 2:
            current = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            change = current - prev
            pct_change = (change / prev) * 100
            return current, change, pct_change
        elif len(df) == 1:
             return df['Close'].iloc[-1], 0.0, 0.0
    except:
        pass

    return 0.0, 0.0, 0.0

def join_metal_data(metals_list, period="5y"):
    """
    Fetches and joins data for multiple metals into a single DataFrame.
    """
    dfs = []
    for metal in metals_list:
        df = get_metal_data(metal, period)
        if df is not None and not df.empty:
            dfs.append(df)
            
    if not dfs:
        return pd.DataFrame()
        
    # Join all dataframes on the Date index
    result = pd.concat(dfs, axis=1)
    return result
