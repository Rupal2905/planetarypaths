import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st

def fetch_nifty_data():
    nifty = yf.download("^NSEI", start="2018-01-08", end="2025-03-10")
    return nifty['Close']

def load_planetary_data(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name=0)
    
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
    
    return df

def main():
    st.title("Planetary Data and Nifty 50 Plot")

    uploaded_file = st.file_uploader("Upload an Excel file with planetary data", type=["xlsx", "xls"])
    
    if uploaded_file is not None:

        df_planetary = load_planetary_data(uploaded_file)

        nifty_data = fetch_nifty_data()

        nifty_data = nifty_data.loc[nifty_data.index >= df_planetary['Date'].min()]
        
        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Planetary Degrees', color='tab:blue')
        ax1.plot(df_planetary['Date'], df_planetary['venus'], label='Venus', color='tab:blue')
        ax1.plot(df_planetary['Date'], df_planetary['mercury'], label='Mercury', color='tab:orange')
        ax1.plot(df_planetary['Date'], df_planetary['sun'], label='Sun', color='tab:red')
        ax1.plot(df_planetary['Date'], df_planetary['saturn'], label='Saturn', color='tab:green')
        ax1.plot(df_planetary['Date'], df_planetary['mars'], label='Mars', color='tab:purple')
        ax1.plot(df_planetary['Date'], df_planetary['rahu'], label='Rahu', color='tab:brown')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Nifty 50 Close Price', color='tab:gray')
        ax2.plot(nifty_data.index, nifty_data.values, label='Nifty 50 Close', color='tab:gray')
        ax2.tick_params(axis='y', labelcolor='tab:gray')
        
