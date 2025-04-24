import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# Load planetary degree data from the Excel file
df_planets = pd.read_excel('eph530n.xlsx')

# Convert 'Date' column to datetime format
df_planets['Date'] = pd.to_datetime(df_planets['Date'], format='%d-%m-%Y')

# Streamlit app interface
st.title('Planetary Degrees and Nifty index OHLC Chart')

index_options = {
    'Nifty 50': '^NSEI',
    'Nifty Next 50': '^NIFTYJR',
    'Nifty 100': '^NIFTY100',
    'Nifty 200': '^NIFTY200',
    'Nifty 500': '^NIFTY500',
    'Nifty Midcap 50': '^CNXMDCP50',
    'Nifty Midcap 100': '^CNXMDCP100',
    'Nifty Midcap 150': '^CNXMDCP150',
    'Nifty Smallcap 50': '^CNXSMALLCAP50',
    'Nifty Smallcap 100': '^CNXSMALLCAP100',
    'Nifty Smallcap 250': '^CNXSMALLCAP250',
    'Nifty LargeMidcap 250': '^CNXLARGEMIDCAP250',
    'Nifty MidSmallcap 400': '^CNXMIDSMALLCAP400',
    'Nifty Bank': '^NSEBANK',
    'Nifty Financial Services': '^CNXFINANCE',
    'Nifty IT': '^CNXIT',
    'Nifty Metal': '^CNXMETAL',
    'Nifty Pharma': '^CNXPHARMA',
    'Nifty FMCG': '^CNXFMCG',
    'Nifty Auto': '^CNXAUTO',
    'Nifty Realty': '^CNXREALTY',
    'Nifty Energy': '^CNXENERGY',
    'Nifty Media': '^CNXMEDIA',
    'Nifty Infra': '^CNXINFRA',
    'Nifty PSU Bank': '^CNXPSUBANK',
    'Nifty Private Bank': '^NIFTY_PRBANK',
    'Nifty Consumer Durables': '^CNXCONSUMERDURABLES',
    'Nifty Oil & Gas': '^CNXOILGAS',
    'Nifty Healthcare': '^CNXHEALTHCARE',
    'Nifty Telecom': '^CNXTELECOM',
    'Nifty Commodities': '^CNXCOMMODITIES',
    'Nifty CPSE': '^CNXCPSE',
    'Nifty MNC': '^CNXMNC',
    'Nifty PSE': '^CNXPSE',
    'Nifty Services Sector': '^CNXSERVICES',
    'Nifty GIFT Nifty': '^NIFTYIFSC'
}


# Sidebar: user inputs for date range
st.sidebar.subheader("Select Index and Date Range")
selected_index = st.sidebar.selectbox("Select Index", list(index_options.keys()))
selected_symbol = index_options[selected_index]

start_date = st.sidebar.date_input("Start Date", datetime(2018, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Filter planetary data to match selected date range
df_planets = df_planets[(df_planets['Date'] >= pd.to_datetime(start_date)) & (df_planets['Date'] <= pd.to_datetime(end_date))]


# Error handling: end date should be after start date
if start_date > end_date:
    st.sidebar.error("End date must be after start date.")

# Sidebar: frequency selection
data_choice = st.sidebar.radio('Select the frequency of Nifty 50 data:', ('Daily', 'Weekly'))

# Determine interval based on selection
interval = '1d' if data_choice == 'Daily' else '1wk'

# Fetch Nifty 50 OHLC data
nifty_data = yf.download(
    selected_symbol,
    start=start_date.strftime('%Y-%m-%d'),
    end=end_date.strftime('%Y-%m-%d'),
    interval=interval, multi_level_index=False
)

# Ensure index is datetime
nifty_data.index = pd.to_datetime(nifty_data.index)

# Filter planetary data to match Nifty index dates if weekly
if data_choice == 'Weekly':
    df_planets = df_planets[df_planets['Date'].isin(nifty_data.index)]

# Merge Close prices into planetary data for display purposes
df_planets = pd.merge(df_planets, nifty_data[['Close']], left_on='Date', right_index=True, how='left')


# Plotting
fig = go.Figure()

# Add planetary degrees
planets = ['venus', 'mercury', 'sun', 'saturn', 'mars', 'rahu']
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']

for planet, color in zip(planets, colors):
    fig.add_trace(go.Scatter(
        x=df_planets['Date'],
        y=df_planets[planet],
        mode='lines',
        name=planet.capitalize(),
        line=dict(color=color)
    ))

# Add candlestick plot for Nifty 50
fig.add_trace(go.Candlestick(
    x=nifty_data.index,
    open=nifty_data['Open'],
    high=nifty_data['High'],
    low=nifty_data['Low'],
    close=nifty_data['Close'],
    name='Nifty 50',
    yaxis='y2'
))

fig.update_layout(
    title=f'Planetary Degrees and Nifty index Candlestick Chart ({data_choice} Data)',
    xaxis_title='Date',
    yaxis_title='Planetary Degrees',
    xaxis=dict(
        rangeslider=dict(visible=False),
        type='date'
    ),
    yaxis2=dict(
        title='Price',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(x=0.01, y=0.99),
    dragmode='zoom',
    hovermode="x unified"
)

# Show plot
st.plotly_chart(fig)

