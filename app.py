import streamlit as st
import pandas as pd
from db import connect_db, save_db

CSV_FILE = "data_siswa.csv"

def load_data():
    df = connect_db(CSV_FILE)
    if df is not None:
        return df
    else:
        return pd.DataFrame(columns=["nim", "nama", "tempat", "tanggal", "kelamin", "agama", "alamat", "telepon"])

def tambah_siswa():
    st.header("Tambah Siswa")
    nim = st.text_input("NIM")
    nama = st.text_input("Nama")
    tempat = st.text_input("Tempat Lahir")
    tanggal = st.date_input("Tanggal Lahir")
    kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    agama = st.text_input("Agama")
    alamat = st.text_area("Alamat")
    telepon = st.text_input("Telepon")

    if st.button("Simpan"):
        df = load_data()
        new_row = {
            "nim": nim,
            "nama": nama,
            "tempat": tempat,
            "tanggal": tanggal.strftime("%Y-%m-%d"),
            "kelamin": kelamin,
            "agama": agama,
            "alamat": alamat,
            "telepon": telepon
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_db(df, CSV_FILE)
        st.success("Data siswa berhasil ditambah")

def ubah_siswa():
    st.header("Ubah Siswa")
    df = load_data()
    if df.empty:
        st.warning("Tidak ada data siswa")
        return

    selected_nim = st.selectbox("Pilih NIM Siswa", df["nim"])
    siswa = df[df["nim"] == selected_nim].iloc[0]

    nama = st.text_input("Nama", siswa["nama"])
    tempat = st.text_input("Tempat Lahir", siswa["tempat"])
    tanggal = st.date_input("Tanggal Lahir", pd.to_datetime(siswa["tanggal"]))
    kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], index=0 if siswa["kelamin"] == "Laki-laki" else 1)
    agama = st.text_input("Agama", siswa["agama"])
    alamat = st.text_area("Alamat", siswa["alamat"])
    telepon = st.text_input("Telepon", siswa["telepon"])

    if st.button("Update"):
        df.loc[df["nim"] == selected_nim, ["nama", "tempat", "tanggal", "kelamin", "agama", "alamat", "telepon"]] = \
            [nama, tempat, tanggal.strftime("%Y-%m-%d"), kelamin, agama, alamat, telepon]
        save_db(df, CSV_FILE)
        st.success("Data siswa berhasil diubah")

def hapus_siswa():
    st.header("Hapus Siswa")
    df = load_data()
    if df.empty:
        st.warning("Tidak ada data siswa")
        return

    selected_nim = st.selectbox("Pilih NIM untuk Dihapus", df["nim"])
    if st.button("Hapus"):
        df = df[df["nim"] != selected_nim]
        save_db(df, CSV_FILE)
        st.success("Data siswa berhasil dihapus")

def main():
    # Header dengan logo UNP
    col1, col2 = st.columns([1, 5])  # kolom kiri lebih kecil
    with col1:
        st.image("logo.png", width=80)  # ganti dengan path/logo sesuai
    with col2:
        st.title("Data Mahasiswa UNP")

    menu = ["Lihat Data", "Tambah Data", "Ubah Data", "Hapus Data"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Lihat Data":
        df = load_data()
        st.dataframe(df if not df.empty else "Belum ada data")

    elif choice == "Tambah Data":
        tambah_siswa()

    elif choice == "Ubah Data":
        ubah_siswa()

    elif choice == "Hapus Data":
        hapus_siswa()

if __name__ == "__main__":
    main()
