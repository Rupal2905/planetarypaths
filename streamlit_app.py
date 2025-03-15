import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st
import matplotlib.dates as mdates
from datetime import datetime

# Load planetary degree data from the Excel file
df_planets = pd.read_excel('eph530n.xlsx')

# Convert 'Date' column to datetime format
df_planets['Date'] = pd.to_datetime(df_planets['Date'], format='%d-%m-%Y')

# Get the current date (dynamic end date)
end_date = datetime.today().strftime('%Y-%m-%d')

# Streamlit interface
st.title('Planetary Degrees and Nifty 50 Close Price')

# Ask user whether to fetch daily or weekly data
data_choice = st.radio('Select the frequency of Nifty 50 data:', ('Daily', 'Weekly'))

# Fetch Nifty 50 data from Yahoo Finance based on user input
start_date = '2018-01-01'

if data_choice == 'Daily':
    nifty_data = yf.download('^NSEI', start=start_date, end=end_date, multi_level_index=False)
elif data_choice == 'Weekly':
    nifty_data = yf.download('^NSEI', start=start_date, end=end_date, interval='1wk', multi_level_index=False)

# Ensure that the Nifty data index is a datetime type and matches the date format in df_planets
nifty_data.index = pd.to_datetime(nifty_data.index)

# If weekly data is selected, filter planetary data to match weekly dates
if data_choice == 'Weekly':
    df_planets = df_planets[df_planets['Date'].isin(nifty_data.index)]

# Merge Nifty 50 close prices with the planetary data (on Date)
df_planets = pd.merge(df_planets, nifty_data[['Close']], left_on='Date', right_index=True, how='left')

# Display the dataframe in the app
st.subheader('Planetary Data and Nifty 50 Close Prices')
st.write(df_planets)

# Plotting with Plotly for interactivity
fig = go.Figure()

# Plot planetary degrees as line plots
fig.add_trace(go.Scatter(x=df_planets['Date'], y=df_planets['venus'], mode='lines', name='Venus', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=df_planets['Date'], y=df_planets['mercury'], mode='lines', name='Mercury', line=dict(color='green')))
fig.add_trace(go.Scatter(x=df_planets['Date'], y=df_planets['sun'], mode='lines', name='Sun', line=dict(color='red')))
fig.add_trace(go.Scatter(x=df_planets['Date'], y=df_planets['saturn'], mode='lines', name='Saturn', line=dict(color='purple')))
fig.add_trace(go.Scatter(x=df_planets['Date'], y=df_planets['mars'], mode='lines', name='Mars', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=df_planets['Date'], y=df_planets['rahu'], mode='lines', name='Rahu', line=dict(color='brown')))

# Add Nifty 50 Close Price as a secondary y-axis
fig.add_trace(go.Scatter(x=df_planets['Date'], y=df_planets['Close'], mode='lines', name='Nifty 50 Close Price', line=dict(color='black'), yaxis='y2'))

# Update layout to set up both axes properly
fig.update_layout(
    title=f'Planetary Degrees and Nifty 50 Close Prices ({data_choice} Data) from 01 Jan 2018 to {end_date}',
    xaxis_title='Date',
    yaxis_title='Planetary Degrees',
    yaxis2=dict(
        title='Nifty 50 Close Price',
        overlaying='y',
        side='right'
    ),
    legend=dict(x=0.01, y=0.99),
    hovermode="x unified"
)

# Show plot in Streamlit app
st.plotly_chart(fig)
