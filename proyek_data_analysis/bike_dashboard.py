import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_dailycount_df(df):
    daily_sharing_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    daily_sharing_df = daily_sharing_df.reset_index()
    daily_sharing_df.rename(columns={
        "dteday": "date",
        "cnt": "sharing_count"
    }, inplace=True)

    return daily_sharing_df

def create_bymonth_df(df):
    bymonth_df = df.groupby(by=['mnth']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
    })
    months= ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    return bymonth_df, months

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
    isworkingday = isworkingday.reset_index()
    isholiday = isholiday.reset_index()
    colors = ["#e8c8d5", "#997d96"]
    labels = ['No', 'Yes']
    
    return isworkingday, isholiday, colors, labels

def create_byweather_df(df):
    byweather_df = df.groupby(by='weathersit').cnt.sum().sort_values(ascending=False)
    colors = ('#f7e0e8', '#ffe4c4', '#cb7489', '#660033')
    explode = (0.1, 0, 0, 0)
    
    return byweather_df, colors, explode

def create_varweather_df(df):
    varweather_df = df.groupby(by=["dteday"]).agg({
        "temp": "mean",
        "atemp": "mean",
        "hum": "mean",
        "windspeed": "mean"
    })
    varweather_df = varweather_df.reset_index()
    return varweather_df

all_df = pd.read_csv("eda_bike_dataset.csv")

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

all_df["dteday"] = pd.to_datetime(all_df["dteday"])
 
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.title("Karisa's Bike Sharing")
    st.image("https://github.com/karisazsh/data-analysis-python/blob/master/proyek_data_analysis/bike-sharing-2.png?raw=true")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_sharing_df = create_dailycount_df(main_df)
bymonth_df, months = create_bymonth_df(main_df)
byday_df = create_byday_df(main_df)
byhourtime_df = create_hourtime_df(main_df)
isworkingday, isholiday, colorsday, labelsday = create_isday_df(main_df)
byweather_df, colorsW, explodeW = create_byweather_df(main_df)
varweather_df = create_varweather_df(main_df)


st.header('Karisa\'s Bike Sharing Dashboard :sparkles::sparkles:')

st.subheader('Daily Orders')

col1, col2, col3 = st.columns(3)
 
with col1:
    total_sharing = daily_sharing_df.sharing_count.sum()
    st.metric("Total sharing", value=total_sharing)
 
with col2:
    total_registered = daily_sharing_df.registered.sum()
    delta_registered = int(daily_sharing_df.registered.sum() / total_sharing * 100 )
    st.metric("Registered Custs", value=total_registered, delta=f'{delta_registered} %')

with col3:
    total_casual = daily_sharing_df.casual.sum()
    delta_casual = int(daily_sharing_df.casual.sum() / total_sharing * 100 )
    st.metric("Casual Custs", value=total_casual, delta=f'{delta_casual} %')


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_sharing_df["date"],
    daily_sharing_df["sharing_count"],
    marker='o', 
    linewidth=2,
    color="#7646ff"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
    
col1, col2 = st.columns([1.2,1], gap="large")
 
with col1:
    fig, ax = plt.subplots(figsize=(13, 10))
    
    y1 = bymonth_df['casual']
    y2 = bymonth_df['registered']
    ax.barh(months, y1, color='#ffe4c4')
    ax.barh(months, y2, left=y1, color='#c77990')
    ax.legend(['Casual', 'Registered'])

    ax.set_title('Bike Sharing Counts per Month', loc="center", fontsize=45)
    ax.invert_yaxis()
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(22, 10))
    
    ax.pie(
        x=byhourtime_df,
        labels=byhourtime_df.index,
        colors=colorsW,
        autopct='%1.1f%%',
        startangle=75,
        wedgeprops = {'width': 0.4},
        textprops={'fontsize': 30}
    )

    ax.set_title("Rent Bike Counts by Hour", loc="center", fontsize=40)
    st.pyplot(fig)


if (len(isworkingday.index) == 2 and len(isholiday.index) == 2):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    
    colors = ["#f7e0e8", "#990cfa"]
    labels = ['No', 'Yes']

    sns.barplot(x=labels, y=isworkingday['cnt'], ax=ax[0], palette=colors, hue=labels)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Working Day", loc="center", fontsize=50)
    ax[0].tick_params(axis ='x', labelsize=40)
    ax[0].tick_params(axis ='y', labelsize=40)
    
    colors = ["#990cfa", "#f7e0e8"]

    sns.barplot(x=labels, y=isholiday['cnt'], ax=ax[1], palette=colors, hue=labels)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Holiday", loc="center", fontsize=50)
    ax[1].tick_params(axis='x', labelsize=40)
    ax[1].tick_params(axis ='y', labelsize=40)

    plt.suptitle("People's day preference to Rent Bike", fontsize=55)

    st.pyplot(fig)


st.subheader("Bike Sharing by Weather")

col1, col2, col3 = st.columns([2,0.8,0.8], gap='large')
 
with col1:
    fig, ax = plt.subplots(figsize=(22, 10))
    colors = ('#feffa3', '#ffe4c4', '#cb7489', '#660033')

    ax.pie(
        x=byweather_df,
        labels=byweather_df.index,
        autopct='%1.2f%%',
        colors=colors,
        textprops={'fontsize': 30}
    )

    # ax.set_title("Weather Preference", loc="center", fontsize=20)
    st.pyplot(fig)
 
with col2:
    min_temp = varweather_df[varweather_df['dteday'] == str(start_date)].temp
    max_temp = varweather_df[varweather_df['dteday'] == str(end_date)].temp
    temp_diff = max_temp.item() - min_temp.item()
    st.metric("Temperature", value="{:.2f}°C".format(max_temp.item()), delta="{:.2f}°C".format(temp_diff))

with col2:
    min_atemp = varweather_df[varweather_df['dteday'] == str(start_date)].atemp
    max_atemp = varweather_df[varweather_df['dteday'] == str(end_date)].atemp
    atemp_diff = max_atemp.item() - min_atemp.item()
    st.metric("Feeling Temperature", value="{:.2f}°C".format(max_atemp.item()), delta="{:.2f}°C".format(atemp_diff))

with col3:
    min_hum = varweather_df[varweather_df['dteday'] == str(start_date)].hum
    max_hum = varweather_df[varweather_df['dteday'] == str(end_date)].hum
    hum_diff = max_hum.item() - min_hum.item()
    st.metric("Humidity", value="{:.2f}".format(max_hum.item()), delta="{:.2f}".format(hum_diff))

with col3:
    min_windspeed = varweather_df[varweather_df['dteday'] == str(start_date)].windspeed
    max_windspeed = varweather_df[varweather_df['dteday'] == str(end_date)].windspeed
    windspeed_diff = max_windspeed.item() - min_windspeed.item()
    st.metric("Wind Speed", value="{:.2f}".format(max_windspeed.item()), delta="{:.2f}".format(windspeed_diff))

fig, ax = plt.subplots(figsize=(16, 8))
degree_sign = u'\N{DEGREE SIGN}'

ax.plot(main_df['dteday'], main_df['temp'], color='#990cfa')
ax.plot(main_df['dteday'], main_df['atemp'], color='#e68585')
ax.set_title(f'Bike Sharing Daily Temperature ({degree_sign}C)',loc="center", fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)