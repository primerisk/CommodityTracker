# Precious Metal Tracker 🪙

A comprehensive dashboard to track historic and current prices of Precious Metals (Gold, Silver, Platinum, Palladium) and Cryptocurrencies (Bitcoin, Ethereum). Built with [Streamlit](https://streamlit.io/) and [yfinance](https://pypi.org/project/yfinance/).

## Features

- **Real-Time Price Tracking**: View up-to-date prices for major metals and crypto assets.
- **Interactive Charts**: Analyze price trends from 1 month to multiple decades.
- **Ratio Analysis**: Calculate and visualize ratios between any two assets (e.g., Gold/Silver Ratio, Bitcoin/Gold Ratio).
- **Customization**: 
    - Dark Mode support.
    - Currency and percentage change normalizations.
- **Asset Metadata**: Includes icons for easy identification.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/precious-metal-tracker.git
    cd precious-metal-tracker
    ```

2.  Install dependencies:
    ```bash
    pip install streamlit yfinance pandas plotly requests
    ```

## Usage

Run the application:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## Technologies

- **Python 3.x**
- **Streamlit**: For the web interface.
- **Plotly**: For interactive charts.
- **Pandas**: For data manipulation.
- **yfinance**: For retrieving market data.

## Note

Data is sourced from Yahoo Finance. This project is for educational and personal use.
