
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent


@st.cache_data
def load_data():
    file_path = BASE_DIR / "main_data.csv"
    data = pd.read_csv(file_path)

    data["dteday"] = pd.to_datetime(data["dteday"])

    # Mengubah kode tahun menjadi tahun sebenarnya
    data["yr"] = data["yr"].map({
        0: 2011,
        1: 2012
    })

    return data


df = load_data()

st.title("🚲 Bike Sharing Dashboard")
st.markdown(
    "Dashboard analisis pola penyewaan sepeda berdasarkan waktu, "
    "hari kerja, musim, dan kondisi cuaca."
)

# Filter tahun
selected_year = st.selectbox(
    "Pilih Tahun",
    options=sorted(df["yr"].dropna().unique())
)

filtered_df = df[df["yr"] == selected_year]

if filtered_df.empty:
    st.warning("Tidak ada data untuk pilihan filter ini.")
    st.stop()

# Ringkasan data
total_rentals = int(filtered_df["cnt"].sum())
average_rentals = filtered_df["cnt"].mean()

peak_hour = int(
    filtered_df.groupby("hr")["cnt"].mean().idxmax()
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", f"{total_rentals:,}")
col2.metric(
    "Rata-rata Penyewaan per Jam",
    f"{average_rentals:,.2f}"
)
col3.metric(
    "Jam dengan Rata-rata Tertinggi",
    f"{peak_hour:02d}:00"
)

st.divider()

# Grafik 1: berdasarkan jam
st.subheader("1. Rata-rata Penyewaan Berdasarkan Jam")

hourly_data = (
    filtered_df.groupby("hr")["cnt"]
    .mean()
    .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(10, 4))

sns.lineplot(
    data=hourly_data,
    x="hr",
    y="cnt",
    marker="o",
    ax=ax1
)

ax1.set_xlabel("Jam")
ax1.set_ylabel("Rata-rata Penyewaan per Jam")
ax1.set_xticks(range(24))
ax1.grid(alpha=0.3)

st.pyplot(fig1)
plt.close(fig1)

# Grafik 2: hari kerja dan non-kerja
st.subheader("2. Penyewaan Berdasarkan Jenis Hari")

working_data = (
    filtered_df.groupby("workingday")["cnt"]
    .mean()
    .reindex([0, 1])
    .rename(index={
        0: "Hari Non-Kerja",
        1: "Hari Kerja"
    })
    .rename_axis("Jenis Hari")
    .reset_index(name="Rata-rata Penyewaan")
)

fig2, ax2 = plt.subplots(figsize=(8, 4))

values = working_data["Rata-rata Penyewaan"].tolist()
labels = working_data["Jenis Hari"].tolist()

max_value = max(values)
colors = [
    "#F58518" if value == max_value else "#4C78A8"
    for value in values
]

ax2.bar(labels, values, color=colors)
ax2.set_xlabel("")
ax2.set_ylabel("Rata-rata Penyewaan per Jam")
ax2.set_title("Perbandingan Rata-rata Penyewaan")

st.pyplot(fig2)
plt.close(fig2)

# Grafik 3: musim
st.subheader("3. Penyewaan Berdasarkan Musim")

season_names = {
    1: "Musim Semi",
    2: "Musim Panas",
    3: "Musim Gugur",
    4: "Musim Dingin"
}

daily_season = (
    filtered_df.groupby("dteday")
    .agg(
        cnt=("cnt", "sum"),
        season=("season", "first")
    )
    .reset_index()
)

season_data = (
    daily_season.groupby("season")["cnt"]
    .mean()
    .rename(index=season_names)
    .rename_axis("Musim")
    .reset_index(name="Rata-rata Penyewaan per Hari")
)

fig3, ax3 = plt.subplots(figsize=(8, 4))

values = season_data["Rata-rata Penyewaan per Hari"].tolist()
labels = season_data["Musim"].tolist()
max_value = max(values)

colors = [
    "#F58518" if value == max_value else "#4C78A8"
    for value in values
]

ax3.bar(labels, values, color=colors)
ax3.set_xlabel("")
ax3.set_ylabel("Rata-rata Penyewaan per Hari")
ax3.set_title("Rata-rata Penyewaan Harian Berdasarkan Musim")

st.pyplot(fig3)
plt.close(fig3)

# Grafik 4: kondisi cuaca
st.subheader("4. Penyewaan Berdasarkan Kondisi Cuaca")

daily_weather = (
    filtered_df.groupby("dteday")
    .agg(
        total_rentals=("cnt", "sum"),
        weather=("weathersit", lambda x: x.mode().iloc[0])
    )
    .reset_index()
)

weather_names = {
    1: "Cerah/Berawan",
    2: "Berkabut",
    3: "Hujan Ringan/Salju Ringan",
    4: "Cuaca Ekstrem"
}

weather_data = (
    daily_weather.groupby("weather")["total_rentals"]
    .mean()
    .rename(index=weather_names)
    .rename_axis("Kondisi Cuaca")
    .reset_index(name="Rata-rata Penyewaan per Hari")
)

fig4, ax4 = plt.subplots(figsize=(10, 4))

values = weather_data["Rata-rata Penyewaan per Hari"].tolist()
labels = weather_data["Kondisi Cuaca"].tolist()
max_value = max(values)

colors = [
    "#F58518" if value == max_value else "#4C78A8"
    for value in values
]

ax4.bar(labels, values, color=colors)
ax4.set_xlabel("")
ax4.set_ylabel("Rata-rata Penyewaan per Hari")
ax4.set_title("Rata-rata Penyewaan Harian Berdasarkan Cuaca")
ax4.tick_params(axis="x", rotation=15)

st.pyplot(fig4)
plt.close(fig4)

st.caption("Sumber data: Bike Sharing Dataset.")
