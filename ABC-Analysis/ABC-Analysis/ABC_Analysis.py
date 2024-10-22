import numpy as np
import pandas as pd
# PN bazli analizde, lead time suresi depo stogunu karsilamali

# parametreler
COLS_ITM = ['PN', 'Avg Lead Time', 'Unit Price', 'Category', '2024 Usage', '2023 Usage', '2022 Usage', '2021 Usage', 'Average Annual Usage']

# dosya ice aktarim
df = pd.read_csv(r'C:\Users\Administrator\Desktop\TEST\DENEME.csv')

# sayisal formata donusturme
df['Unit Price'] = df['Unit Price'].astype(str).str.replace(',', '.').astype(float)
df['Avg Lead Time'] = df['Avg Lead Time'].astype(str).str.replace(',', '.').astype(float)
df['Average Annual Usage'] = df['Average Annual Usage'].astype(str).str.replace(',', '.').astype(float)

# min-max normalizasyon
df['Unit Price Normalized'] = (df['Unit Price'] - df['Unit Price'].min()) / (df['Unit Price'].max() - df['Unit Price'].min())
df['Avg Lead Time Normalized'] = (df['Avg Lead Time'] - df['Avg Lead Time'].min()) / (df['Avg Lead Time'].max() - df['Avg Lead Time'].min())
df['Average Annual Usage Normalized'] = (df['Average Annual Usage'] - df['Average Annual Usage'].min()) / (df['Average Annual Usage'].max() - df['Average Annual Usage'].min())

# katsayilar, oneme gore sonradan degistirilebilir
w1 = 0.5  # Unit Price katsayisi
w2 = 0.3  # Average Annual Usage katsayisi
w3 = 0.2  # Avg Lead Time katsayisi

# onem puanı hesaplama
df['Score'] = (w1 * df['Unit Price Normalized']) + (w2 * df['Average Annual Usage Normalized']) + (w3 * df['Avg Lead Time Normalized'])

# puanlara gore kategorizasyon
df['ABC Categorization'] = pd.qcut(df['Score'], q=[0, 0.2, 0.5, 1], labels=['A', 'B', 'C'])

# ceyreklik kullanim hesaplama
df['Quarterly Usage'] = df['Average Annual Usage'] / 4

# ABC kategorisine gore RL belirleme
def calculate_reorder_level(row):
    lead_time = row['Avg Lead Time']
    quarterly_usage = row['Quarterly Usage']
    
    # ABC kategorisine gore guvenlik stogu belirleme
    if row['ABC Categorization'] == 'A':
        safety_stock = quarterly_usage * 0.8  # A kategori icin yuksek seviye guvenlik stogu carpan 0.8
    elif row['ABC Categorization'] == 'B':
        safety_stock = quarterly_usage * 0.6  # B kategori icin orta seviye guvenlik stogu carpan 0.6
    else:
        safety_stock = quarterly_usage * 0.5   # C kategori icin dusuk seviye guvenlik stogu carpan 0.5
    
    # reorder level hesaplama
    # buraya bi revize
    reorder_level = (row['Average Annual Usage'] * lead_time / 90) + safety_stock
    return reorder_level
    # buraya bi revize
    # 2024%60 kullanım # 2023%40 kullanım

# Reorder Level sutunu ekleme
df['Reorder Level'] = df.apply(calculate_reorder_level, axis=1)

# dosya kaydetme
df.to_csv(r'C:\Users\Administrator\Desktop\TEST\DENEME_output_reorder.csv', index=False)

print("ABC Kategorilendirme ve Reorder Level hesaplamaları tamamlandı ve dosya kaydedildi.")
