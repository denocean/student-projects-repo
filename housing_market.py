import pandas as pd
from prophet import Prophet
import streamlit as st
# 1. Load Data
@st. cache_data
def load_data ():
    # Replace this with real Zillow/FRED CSV later
    data = {
        "ds": pd. date_range ("2010-01-01", periods=15, freq="Y"),
        "y": [
            180000, 190000, 200000, 210000, 220000,
            230000, 250000, 270000, 290000, 310000,
            340000, 370000, 400000, 420000, 440000
        ]
    }
    return pd.DataFrame(data)
df = load_data()

# 2. Forecast Function
def make forecast (data, years=5):
    m = Prophet (yearly seasonality=False, daily seasonality=False)
    m.fit(data)

    future = m.make_future_dataframe(periods=years, freq="Y")
    forecast = m.predict(future)
    return forecast

forecast = make_forecast(df, years=5)

# 3.  Summary
def summarize_forecast(forecast_df, history_df):
    start_year = history_df["ds"].dt.year.min()
    end_year = forecast_df["ds"]. dt.year.max()
    growth = (forecast_df["yhat"].iloc[-1] / history_df["y"].iloc[0] - 1) * 100

    return (
        f"Between {start_year} and {end_year}, housing prices are projected "
        f"to increase by approximately {growth:.2f}%. "
        "This trend indicates sustained upward momentum in the market, "
        "though affordability challenges and regional differences may persist."
    )

summary_text = summarize_forecast(forecast, df)

# 4. Streamlit Dashboard
st.set_page_config (page_title="Housing Market Forecast", layout="wide")
st. title ("U.S. Housing Market Forecast Dashboard")

st.subheader(" Historical Data")
st. line_chart(df.set_index("ds”) ["y"])

st. sub header(" Forecasted Prices")
st. line chart(forecast.set_index("ds")[["yhat", "yhat_lower", "yhat_upper"]])

st. write(summary_text)

# 5. Upload Your Own Data

st.subheader(" Upload Your Own Data")
uploaded_file = st. file_uploader ("Upload a CSV with columns: ds (date), y (price)", type="csv")

if uploaded_file is not None:
    user_df = pd. read_csv (uploaded_file, parse_dates=["ds"])
    st. write ("Preview of uploaded data:", user_df. head ())

    user_forecast = make_forecast (user_df, years=5)
    user_summary = summarize_forecast(user_forecast, user_df)

    st. line chart(user_df.set_index("ds”) ["y"])
    st. line_chart(user_forecast.set_index("ds”) [["yhat", "yhat_lower", "yhat_upper"]])
    st. write (" Summary:", user_summary