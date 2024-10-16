import numpy as np
import pandas as pd

# Parametreler
COLS_ITM = ['PN', 'Avg Lead Time', 'Unit Price', 'Category', '2024 Usage', '2023 Usage', '2022 Usage', '2021 Usage', 'Average Annual Usage']  # Parca tanimlama

# Dosya ice aktarimi
df = pd.read_csv(r'C:\Users\Administrator\Desktop\TEST\DENEME.csv')

# Yeni 'id' sutunu olusturma
df['id'] = df['Avg Lead Time'].astype(str) + '-' + df['Unit Price'].astype(str)

# ABC kategorilendirme fonksiyonu
def categorize(row):
    # Esik degerleri, Unit Price, Average Annual Usage ve Avg Lead Time icin median uzerinden yapilacak
    price_threshold = df['Unit Price'].median()  # ortanca fiyat
    usage_threshold = df['Average Annual Usage'].median()  # ortanca kullanim
    lead_time_threshold = df['Avg Lead Time'].median()  # ortanca teslim suresi

    # Kosullar
    if (row['Unit Price'] > price_threshold and 
        row['Average Annual Usage'] > usage_threshold and 
        row['Avg Lead Time'] > lead_time_threshold):
        return 'A'
    elif ((row['Unit Price'] > price_threshold and row['Average Annual Usage'] <= usage_threshold) or 
          (row['Unit Price'] <= price_threshold and row['Avg Lead Time'] > lead_time_threshold)):
        return 'B'
    else:
        return 'C'

# Kategorilendirme sutunu olusturma
df['ABC Categorization'] = df.apply(categorize, axis=1)

# Veri cercevesini excel dosyasına kaydetme
df.to_csv(r'C:\Users\Administrator\Desktop\TEST\DENEME_output.csv')

print("ABC Kategorilendirmesi tamamlandı ve dosya kaydedildi.")
