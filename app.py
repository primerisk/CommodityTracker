import requests
import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import get_current_price, join_metal_data, TICKERS, get_ticker_metrics

st.set_page_config(page_title="Precious Metal Tracker", layout="wide", page_icon="🪙")

@st.cache_data(ttl=300)
def get_public_ip():
    """Fetches the requestor's public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return "Unknown"

@st.cache_data(ttl=300)
def fetch_data_with_timestamp(tickers, period):
    """Fetches data and returns it with a timestamp."""
    df = join_metal_data(tickers, period)
    return df, datetime.datetime.now()

def configure_chart_axis(fig, period):
    """
    Configures the x-axis ticks based on the selected period.
    - Max: Decades (10 years)
    - <= 1 Year: Months
    - > 1 Year: Years
    """
    if period == "max":
        # Decades: 10 years = 120 months
        fig.update_xaxes(dtick="M120", tickformat="%Y")
    elif period in ["1mo", "3mo", "6mo", "1y"]:
        # Months
        fig.update_xaxes(dtick="M1", tickformat="%b %Y")
    else:
        # Years (2y, 5y, 10y)
        fig.update_xaxes(dtick="M12", tickformat="%Y")


def swap_assets():
    st.session_state.num, st.session_state.den = st.session_state.den, st.session_state.num

def main():
    # --- Dark Mode Logic ---
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    def toggle_dark_mode():
        st.session_state.dark_mode = not st.session_state.dark_mode

    # Top Right Button
    col_title, col_toggle = st.columns([9, 1])
    with col_title:
        st.title("🪙 Asset Tracker (Metals & Crypto)")
    with col_toggle:
        mode_icon = "🌞" if not st.session_state.dark_mode else "Hz"
        if st.button("🌓", help="Toggle Dark Mode", on_click=toggle_dark_mode):
            pass

    # CSS Injection
    if st.session_state.dark_mode:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            [data-testid="stSidebar"] {
                background-color: #262730;
                color: #FAFAFA;
            }
            .stMetric {
                background-color: #262730; 
                padding: 10px;
                border-radius: 5px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        chart_template = "plotly_dark"
    else:
        chart_template = "plotly"

    st.markdown("Track historic and current prices of Precious Metals and Cryptocurrencies, and analyze their ratios.")

    # --- Sidebar ---
    st.sidebar.header("Configuration")
    period_options = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"]
    selected_period = st.sidebar.selectbox("Select History Period", period_options, index=5)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "Data sourced from Yahoo Finance via `yfinance`.\n"
        "Prices are typically for Futures Contracts (e.g. GC=F, SI=F)."
    )

    # --- Metrics Section ---
    st.subheader("Current Market Prices (Approx.)")
    
    cols = st.columns(len(TICKERS))
    for i, metal in enumerate(TICKERS.keys()):
        price, change, pct_change = get_ticker_metrics(metal)
        with cols[i]:
            # Nested columns for Icon + Metric
            c_img, c_met = st.columns([1, 2])
            with c_img:
                st.image(f"assets/{metal}.png", use_container_width=True)
            with c_met:
                st.metric(label=metal, value=f"${price:,.2f}", delta=f"{change:,.2f} ({pct_change:.2f}%)")

    # --- Data Fetching ---
    with st.spinner(f"Fetching historical data ({selected_period})..."):
        df, fetch_time = fetch_data_with_timestamp(list(TICKERS.keys()), period=selected_period)

    if df.empty:
        st.error("Could not fetch data. Please check your internet connection or try a different period.")
        return

    st.markdown("---")

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs(["📈 Price Trends", "➗ Ratio Analysis", "📄 Raw Data"])

    # --- Tab 1: Price Trends ---
    with tab1:
        st.subheader(f"Price Trends ({selected_period})")
        
        # Normalize toggle
        normalize = st.checkbox("Normalize to % Change (Compare Relative Growth)", value=False)
        
        plot_df = df.copy()
        if normalize:
            # (Price - StartPrice) / StartPrice * 100
            plot_df = (plot_df / plot_df.iloc[0] * 100) - 100
            y_axis_title = "% Change"
            format_str = ".2f"
        else:
            y_axis_title = "Price (USD)"
            format_str = None

        fig = px.line(plot_df, x=plot_df.index, y=plot_df.columns, title="Asset Prices", markers=False)
        fig.update_layout(xaxis_title="Date", yaxis_title=y_axis_title, hovermode="x unified", template=chart_template)
        configure_chart_axis(fig, selected_period)
        if normalize:
            fig.update_yaxes(ticksuffix="%")
        
        st.plotly_chart(fig, use_container_width=True)

    # --- Tab 2: Ratio Analysis ---
    with tab2:
        st.subheader("Gold / Silver Ratio & Others")
        
        # Initialize session state for selectors if not present
        if "num" not in st.session_state:
            st.session_state.num = "Gold"
        if "den" not in st.session_state:
            st.session_state.den = "Silver"

        # Layout: Img1 - Select1 - Swap - Select2 - Img2
        c1, c2, c3, c4, c5 = st.columns([1, 3, 1, 3, 1])
        
        with c1:
            st.image(f"assets/{st.session_state.num}.png", use_container_width=True)
            
        with c2:
            st.selectbox("Numerator", list(TICKERS.keys()), key="num")

        with c3:
            st.write("")
            st.write("")
            st.button("↔", help="Swap", on_click=swap_assets)

        with c4:
            st.selectbox("Denominator", list(TICKERS.keys()), key="den")
            
        with c5:
            st.image(f"assets/{st.session_state.den}.png", use_container_width=True)

        ratio_choice_1 = st.session_state.num
        ratio_choice_2 = st.session_state.den

        if ratio_choice_1 == ratio_choice_2:
            st.warning("Select different assets to calculate a ratio.")
        else:
            ratio_name = f"{ratio_choice_1} / {ratio_choice_2} Ratio"
            ratio_series = df[ratio_choice_1] / df[ratio_choice_2]
            
            # Statistics
            curr_ratio = ratio_series.iloc[-1]
            avg_ratio = ratio_series.mean()
            min_ratio = ratio_series.min()
            max_ratio = ratio_series.max()
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Current Ratio", f"{curr_ratio:.4f}")
            c2.metric("Average", f"{avg_ratio:.4f}")
            c3.metric("Min", f"{min_ratio:.4f}")
            c4.metric("Max", f"{max_ratio:.4f}")

            # Chart
            fig_ratio = px.line(x=ratio_series.index, y=ratio_series.values, title=f"Historical {ratio_name}")
            fig_ratio.update_layout(xaxis_title="Date", yaxis_title="Ratio", hovermode="x unified", template=chart_template)
            configure_chart_axis(fig_ratio, selected_period)
            
            # Add average line
            fig_ratio.add_hline(y=avg_ratio, line_dash="dash", line_color="red", annotation_text="Average")
            
            st.plotly_chart(fig_ratio, use_container_width=True)

    # --- Tab 3: Raw Data ---
    with tab3:
        st.subheader("Historical Data")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

    # --- Footer ---
    st.markdown("---")
    
    # Calculate time since update
    time_since_update = datetime.datetime.now() - fetch_time
    # Format to HH:MM:SS
    # timedelta string is usually "days, HH:MM:SS.micro" or "HH:MM:SS.micro"
    # We just want HH:MM:SS
    ts_str = str(time_since_update).split('.')[0]
    if "day" not in ts_str and len(ts_str.split(':')) == 3:
         ts_str = ts_str # simple case
    
    ip_address = get_public_ip()
    
    footer_col1, footer_col2 = st.columns(2)
    with footer_col1:
        st.caption(f"Time since last update: {ts_str}")
    with footer_col2:
        st.caption(f"Requestor IP: {ip_address}")

if __name__ == "__main__":
    main()
