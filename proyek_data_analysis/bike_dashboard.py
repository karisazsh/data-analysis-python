import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_bymonth_df(df):
    bymonth_df = df.groupby(by=['mnth']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
    })
    
    return bymonth_df

def create_byday_df(df):
    byday_df = df.groupby(by=['mnth']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
    })
    
    return byday_df

def create_hourtime_df(df):
    hour_time_df = df.groupby(by='hour_time').cnt.sum()
    hour_time_df = hour_time_df.reindex(index= ['Morning', 'Afternoon', 'Evening', 'Night'])
    
    return hour_time_df

def create_isday_df(df):
    isworkingday = df.groupby(by=['workingday']).cnt.sum()
    isholiday = df.groupby(by=['holiday']).cnt.sum()
    colors = ["#e8c8d5", "#997d96"]
    labels = ['No', 'Yes']
    
    return isworkingday, isholiday, colors, labels

def create_byweather_df(df):
    byweather_df = df.groupby(by='weathersit').cnt.sum().sort_values(ascending=False)
    colors = ('#f7e0e8', '#ffe4c4', '#cb7489', '#660033')
    explode = (0.1, 0, 0, 0)
    
    return byweather_df, colors, explode

all_df = pd.read_csv("eda_bike_dataset.csv")

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

all_df["dteday"] = pd.to_datetime(all_df["dteday"])
 
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://drive.google.com/file/d/1s_DqpZnNPqRFGDz0NV0hlAnZVM1UuSz4/view?usp=sharing")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

bymonth_df = create_bymonth_df(main_df)
byday_df = create_byday_df(main_df)
byhourtime_df = create_hourtime_df(main_df)
isworkingday, isholiday, colorsday, labelsday = create_isday_df(main_df)
byweather_df, colorsW, explodeW = create_byweather_df(main_df)


st.header('Dicoding Collection Dashboard :sparkles:')

st.subheader('Daily Orders')