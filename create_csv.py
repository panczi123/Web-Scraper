import pandas as pd

def create_csv():
    # Create data
    data = {
        'Company name': ['iZabudowy', 'Bemet'],
        'Website': ['http://www.izabudowy.pl', 'http://www.bemet.pl/']
    }

    # Create a dataframe from the data
    df = pd.DataFrame(data)

    # Save the dataframe to a .csv file
    df.to_csv('csv_links.csv', index=False)
