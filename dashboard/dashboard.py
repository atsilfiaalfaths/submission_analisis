import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
from babel.numbers import format_currency
sns.set(style='dark')



rent_day_df = pd.read_csv("./data/real_day.csv")

datetime_columns = ["dateday"]
for column in datetime_columns:
    rent_day_df[column] = pd.to_datetime(rent_day_df[column])


rent_day_df.sort_values(by="dateday", inplace=True)
rent_day_df.reset_index(inplace=True)



# function 
# Menyiapkan daily_rent_df
def create_daily_rent_df(d_df):
    daily_rent_df = d_df.groupby(by='dateday').agg({
        'total_count_user': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_registered_rent_df
def create_registered_rent_df(d_df):
    daily_registered_rent_df = d_df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Menyiapkan daily_casual_rent_df
def create_casual_rent_df(d_df):
    daily_casual_rent_df = d_df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df


# monthly
def create_season_rent_df(d_df):
    season_rent_df = d_df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

min_date =rent_day_df["dateday"].min()
max_date = rent_day_df["dateday"].max()


 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Range Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


day_main_df = rent_day_df[(rent_day_df['dateday'] >= str(start_date)) & 
                (rent_day_df['dateday'] <= str(end_date))]

# call
daily_rent_df = create_daily_rent_df(day_main_df)
daily_registered_rent_df = create_registered_rent_df(day_main_df)
daily_casual_rent_df = create_casual_rent_df(day_main_df)
monthly_rent_df = create_monthly_rent_df(day_main_df)


st.header('Ats BR Dashboard 🚲')


st.subheader('Daily Orders')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    daily_casual_rent_total = daily_casual_rent_df ['casual'].sum()
    st.metric('Total Casual', value=daily_casual_rent_total)
 
with col2:
    daily_registered_rent_total = daily_registered_rent_df['registered'].sum()
    st.metric('Total Register', value=daily_registered_rent_total)

with col3:
    daily_rent_total = daily_rent_df['total_count_user'].sum()
    st.metric('Total User', value= daily_rent_total)








