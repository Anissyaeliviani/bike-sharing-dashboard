
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
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df


df = load_data()

st.title("🚲 Bike Sharing Dashboard")
st.markdown(
    "Dashboard analisis pola penyewaan sepeda berdasarkan waktu, "
    "hari kerja, musim, dan kondisi cuaca."
)

# Filter tahun
st.sidebar.header("Filter Data")

year_options = sorted(df["yr"].unique().tolist())
selected_years = st.sidebar.multiselect(
    "Pilih tahun",
    options=year_options,
    default=year_options
)

filtered_df = df[df["yr"].isin(selected_years)]

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
col2.metric("Rata-rata Penyewaan per Jam", f"{average_rentals:,.2f}")
col3.metric("Jam dengan Rata-rata Tertinggi", f"{peak_hour:02d}:00")

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
ax1.set_ylabel("Rata-rata Penyewaan")
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
    .rename(index={0: "Hari Non-Kerja", 1: "Hari Kerja"})
    .rename_axis("Jenis Hari")
    .reset_index(name="Rata-rata Penyewaan")
)

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=working_data,
    x="Jenis Hari",
    y="Rata-rata Penyewaan",
    hue="Jenis Hari",
    legend=False,
    ax=ax2
)
ax2.set_xlabel("")
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

season_data = (
    filtered_df.groupby("season")["cnt"]
    .mean()
    .rename(index=season_names)
    .rename_axis("Musim")
    .reset_index(name="Rata-rata Penyewaan")
)

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=season_data,
    x="Musim",
    y="Rata-rata Penyewaan",
    hue="Musim",
    legend=False,
    ax=ax3
)
ax3.set_xlabel("")
st.pyplot(fig3)
plt.close(fig3)

# Grafik 4: kondisi cuaca
st.subheader("4. Penyewaan Berdasarkan Kondisi Cuaca")

weather_names = {
    1: "Cerah",
    2: "Berkabut/Berawan",
    3: "Hujan Ringan/Salju",
    4: "Hujan Lebat/Salju"
}

weather_data = (
    filtered_df.groupby("weathersit")["cnt"]
    .mean()
    .rename(index=weather_names)
    .rename_axis("Kondisi Cuaca")
    .reset_index(name="Rata-rata Penyewaan")
)

fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.barplot(
    data=weather_data,
    x="Kondisi Cuaca",
    y="Rata-rata Penyewaan",
    hue="Kondisi Cuaca",
    legend=False,
    ax=ax4
)
ax4.set_xlabel("")
ax4.tick_params(axis="x", rotation=15)
st.pyplot(fig4)
plt.close(fig4)

st.caption("Sumber data: Bike Sharing Dataset.")
