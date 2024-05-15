import pandas as pd

data = {
    'Company name': ['iZabudowy', 'Bemet'],
    'Website': ['http://www.izabudowy.pl', 'http://www.bemet.pl/']
}
df = pd.DataFrame(data)
df.to_csv('csv_links.csv', index=False)
