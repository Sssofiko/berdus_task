import pandas as pd

df = pd.read_excel('DataSet.ods', engine='odf')

# Очистка данных
df = df[df['CVE-ID'] != 'NVD-CWE-Other']
df = df[df['CVSS-V3'] != 'None']

df.to_csv('cleaned_data.csv', index=False)

print("Очищенные данные сохранены в файл 'cleaned_data.csv'.")
