# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis data penyewaan sepeda menggunakan Bike Sharing Dataset. Analisis dilakukan untuk mengetahui pola penyewaan sepeda berdasarkan jam, jenis hari, musim, dan kondisi cuaca selama periode Januari 2011 hingga Desember 2012.

Hasil analisis digunakan untuk memahami pola permintaan penyewaan sepeda dan memberikan rekomendasi terkait ketersediaan sepeda.

## Pertanyaan Bisnis

1. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda per jam antara hari kerja dan hari nonkerja, serta pada jam berapa penyewaan mencapai puncaknya pada masing-masing jenis hari selama periode Januari 2011 hingga Desember 2012?
2. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda per hari berdasarkan musim dan kondisi cuaca selama periode Januari 2011 hingga Desember 2012, serta bagaimana hasilnya dapat digunakan untuk merencanakan ketersediaan sepeda?

## Struktur Direktori

- `dashboard/`: berisi aplikasi dashboard dan data yang digunakan dashboard.
- `data/`: berisi dataset yang digunakan untuk analisis.
- `notebook.ipynb`: berisi proses pengolahan dan analisis data.
- `requirements.txt`: berisi daftar library Python beserta versinya.
- `url.txt`: berisi tautan dashboard yang telah dipublikasikan.

## Instalasi dan Persiapan Environment

### 1. Menggunakan Anaconda

Buat environment Python baru:

```bash
conda create --name main-ds python=3.9
```

Aktifkan environment:

```bash
conda activate main-ds
```

Masuk ke direktori proyek yang berisi file `requirements.txt`, kemudian jalankan:

```bash
pip install -r requirements.txt
```

### 2. Menjalankan Dashboard

Dari direktori utama proyek, jalankan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka melalui browser. Jika browser tidak terbuka otomatis, ikuti alamat lokal yang ditampilkan di terminal.

## Menjalankan Notebook

Buka file `notebook.ipynb` menggunakan Jupyter Notebook, JupyterLab, atau Google Colab untuk melihat proses pengolahan data, analisis, visualisasi, dan kesimpulan.

## Hasil Analisis

Analisis mencakup pola rata-rata penyewaan sepeda berdasarkan jam dan jenis hari, serta perbandingan rata-rata penyewaan harian berdasarkan musim dan kondisi cuaca.

Dashboard interaktif disediakan untuk membantu pengguna mengeksplorasi hasil analisis tersebut.
