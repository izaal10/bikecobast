import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    return df

df = load_data()


# atur tema
sns.set_theme(style="dark")

# Mapping label untuk weather situation
weather_mapping = {
    1: 'Clear, Few clouds',
    2: 'Mist, Cloudy',
    3: 'Light Snow / Rain',
    4: 'Heavy Rain, Ice Pallets'
}

# Mengganti nilai weathersit dengan label yang baru
df['weathersit'] = df['weathersit'].map(weather_mapping)


# Judul dashboard
st.title('Hello World')

# Tampilkan data frame jika dipilih
if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.dataframe(df)

# Pilihan multiselect untuk musim
season_label_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
selected_seasons = st.sidebar.multiselect('Select Seasons:', df['season'].unique(), format_func=lambda x: season_label_mapping[x])

# Pilihan multiselect untuk tahun
year_label_mapping = {0: 2011, 1: 2012}
selected_years = st.sidebar.multiselect('Select Years:', df['yr'].unique(), format_func=lambda x: year_label_mapping[x])

# Filter data berdasarkan pilihan pengguna
filtered_df = df[(df['season'].isin(selected_seasons)) & (df['yr'].isin(selected_years))]

# Membuat subplot untuk grafik
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(12, 18))

# Grafik jumlah penyewaan sepeda (cnt, registered, dan casual)
sns.lineplot(x='mnth', y='cnt', data=filtered_df, label='Total Rentals', ax=axes[0])
sns.lineplot(x='mnth', y='registered', data=filtered_df, label='Registered Rentals', ax=axes[0])
sns.lineplot(x='mnth', y='casual', data=filtered_df, label='Casual Rentals', ax=axes[0])
axes[0].set_title('Bike Rental Counts Over Time')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Count')
axes[0].legend(loc='upper left')

# Grafik suhu dan kelembaban
sns.lineplot(x='mnth', y='temp', data=filtered_df, label='Temperature', ax=axes[1])
sns.lineplot(x='mnth', y='hum', data=filtered_df, label='Humidity', ax=axes[1])
sns.lineplot(x='mnth', y='windspeed', data=filtered_df, label='Wind Speed', ax=axes[1])
axes[1].set_title('Temperature and Humidity Over Time')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Normalized Values')
axes[1].legend(loc='upper left')

# Grafik cuaca
sns.countplot(x='weathersit', data=filtered_df, ax=axes[2])
axes[2].set_title('Weather Situation Distribution')
axes[2].set_xlabel('Weather Situation')
axes[2].set_ylabel('Count')
axes[2].tick_params(axis='x')  

# Grafik jumlah peminjaman berdasarkan hari libur dan hari kerja
filtered_df['holiday'] = filtered_df['holiday'].replace({0: 'Work Day', 1: 'Holiday'})
sns.barplot(x='holiday', y='cnt', data=filtered_df, errorbar=None, ax=axes[3])
axes[3].set_title('Bike Rental Counts on Working Days and Holidays')
axes[3].set_xlabel('Day Type')
axes[3].set_ylabel('Count')

# Adjust layout
plt.tight_layout()

# Gunakan st.pyplot(fig) untuk menggambarkan plot
st.pyplot(fig)
