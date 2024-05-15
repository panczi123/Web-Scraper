import pandas as pd

# Stwórz słownik z danymi
data = {
    'Company name': ['iZabudowy', 'Bemet'],
    'Website': ['http://www.izabudowy.pl', 'http://www.bemet.pl/']
}
print(data)
# Stwórz DataFrame z danymi
df = pd.DataFrame(data)

print(df)

# Zapisz DataFrame do pliku .csv
df.to_csv('csv_links.csv', index=False)
