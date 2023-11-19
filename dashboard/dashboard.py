import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')



rent_day_df = pd.read_csv("./dashboard/main_data.csv")

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

def create_monthly_rent_df(d_df):
    monthly_rent_df = d_df.groupby(by=["year", "month"]).agg({
        'total_count_user': 'sum'
    }).reset_index()
    return monthly_rent_df
   

# monthly
def create_season_rent_df(d_df):
    season_rent_df = d_df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

def create_weathersit_rent_df(d_df):
    weathersit_rent_df = d_df.groupby(by='weathersit')[['registered', 'casual']].sum().reset_index()
    return weathersit_rent_df

def create_workingday_rent_df(d_df):
    workingday_rent_df = d_df.groupby(by='workingday')[['total_count_user']].sum().reset_index()
    return workingday_rent_df


def create_holiday_rent_df(d_df):
    holiday_rent_df = d_df.groupby(by='holiday')[['total_count_user']].sum().reset_index()
    return holiday_rent_df

def create_weekday_rent_df(d_df):
    custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    weekday_rent_df = d_df.groupby(by='day_name')[['total_count_user']].sum().reset_index()
    weekday_rent_df['day_name'] = pd.Categorical(weekday_rent_df['day_name'], categories=custom_order, ordered=True)

    return weekday_rent_df




min_date =rent_day_df["dateday"].min()
max_date = rent_day_df["dateday"].max()


 
with st.sidebar:
    # Menambahkan logo perusahaan
    # st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.image("https://raw.githubusercontent.com/atsilfiaalfaths/submission_analisis/main/dashboard/abr.png?token=GHSAT0AAAAAACJYSEDZHBAI3AELK6O6PS7GZKZTW2A")
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
season_rent_df = create_season_rent_df(day_main_df)
weathersit_rent_df = create_weathersit_rent_df(day_main_df)
workingday_rent_df = create_workingday_rent_df(day_main_df)
holiday_rent_df = create_holiday_rent_df(day_main_df)
weekday_rent_df = create_weekday_rent_df(day_main_df)


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


# plot total perfilter day
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dateday"],
    daily_rent_df["total_count_user"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Grafik user", loc="center", fontsize=30)
ax.set_xlabel("Rentang waktu")
ax.set_ylabel("Jumlah user")
st.pyplot(fig)


# plot monthly
fig, ax = plt.subplots(figsize=(16, 12))
months_order = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="month", 
    y="total_count_user",
    data= monthly_rent_df.sort_values(by="total_count_user", ascending=False),
    palette=colors,
    ax=ax,
    order=months_order
)
ax.set_title("Monthly Rentals", loc="center", fontsize=30)
ax.set_ylabel("Month")
ax.set_xlabel("Total user")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.subheader('Per season')
col1, col2= st.columns(2)
 
with col1:
    st.subheader('Register user ')
    # plot season regiestered user
    fig, ax = plt.subplots(figsize=(16, 12))

    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]
    sorted_r_df = season_rent_df.sort_values(by="registered", ascending=False)
    sns.barplot(
        x="season", 
        y="registered",
        data= sorted_r_df,
        palette=colors,
        ax=ax,
    )
    for index, row in enumerate(sorted_r_df['registered']):
        ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
  
    ax.set_title(" Register user Rentals in Season", loc="center", fontsize=30)
    ax.set_ylabel("Month")
    ax.set_xlabel("Total Registered user")
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

with col2:
    st.subheader('Casual user ')

    # plot season registered user
    fig, ax = plt.subplots(figsize=(15, 10))

    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]
    sorted_df = season_rent_df.sort_values(by="casual", ascending=False)
    sns.barplot(
        x="season", 
        y="casual",
        data=sorted_df,
        palette=colors,
        ax=ax,
    )
    for index, row in enumerate(sorted_df['casual']):
        ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
  
    ax.set_title("Casual user rental in season", loc="center", fontsize=30)
    ax.set_ylabel("Total casual user")
    ax.set_xlabel("Month")
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

    

st.subheader('Weatehersit rentals')
# plot weathersit season per category user
fig, ax = plt.subplots(figsize=(16, 8))
sorted_wc_df = weathersit_rent_df.sort_values(by=["registered", "casual"], ascending=False)
# sorted_wr_df = weathersit_rent_df.sort_values(by="registered", ascending=False)
sns.barplot(
    x='weathersit',
    y='registered',
    data=sorted_wc_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='weathersit',
    y='casual',
    data=sorted_wc_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

for index, row in enumerate(sorted_wc_df['registered']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)


for index, row in enumerate(sorted_wc_df['casual']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel("Weathersit (Cuaca)")
ax.set_ylabel("Total user")
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# plot holiday, working day, weekday
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))

colors1=["#508D69", "#9ADE7B"]
colors2=["#0766AD", "#29ADB2"]
colors3=["#F1C93B", "#FBD85D", "#F7D060", "#FDFFAE", "#E7B10A", "#F7C04A", "#F7DB6A"]

# Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='total_count_user',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent_df['total_count_user']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
  x='holiday',
  y='total_count_user',
  data=holiday_rent_df,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(holiday_rent_df['total_count_user']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
sorted_weekday_df = weekday_rent_df.sort_values(by=["day_name"], ascending=True)

sns.barplot(
  x='day_name',
  y='total_count_user',
  data=sorted_weekday_df,
  palette=colors3,
  ax=axes[2],
  )

for index, row in enumerate(sorted_weekday_df['total_count_user']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Atsilfia Alfath Syam 2023')