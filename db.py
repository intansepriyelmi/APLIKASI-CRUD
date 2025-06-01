import pandas as pd

def connect_db(csv_file="data_siswa.csv"):
    try:
        df = pd.read_csv(csv_file)
        return df
    except FileNotFoundError:
        # Jika belum ada, kembalikan DataFrame kosong dengan header yang sesuai
        columns = ["nim", "nama", "tempat", "tanggal", "kelamin", "agama", "alamat", "telepon"]
        return pd.DataFrame(columns=columns)
    except Exception as e:
        print(f"Gagal membaca file CSV: {e}")
        return None

def save_db(df, csv_file="data_siswa.csv"):
    try:
        df.to_csv(csv_file, index=False)
    except Exception as e:
        print(f"Gagal menyimpan data ke CSV: {e}")
