import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://slusi.dacnet.nic.in/dmwai/MAHARASHTRA/District/PUNE.html"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    area_elements = soup.select('map[name="mapmap"] area')

    # 'href' values structure: watershed/4D5H7.html

    # Extracting watershed IDs from the 'href' attribute of each 'area' element
    watershed_ids = [area['href'].split(
        '/')[-1].split('.')[0] for area in area_elements]

    df = pd.DataFrame(watershed_ids, columns=['Watershed_ID'])

    print("Unique IDs: ", df["Watershed_ID"].unique())
    print("Length of unique IDs: ", len(df["Watershed_ID"].unique()))

    uniqueIdDF = pd.DataFrame(
        df["Watershed_ID"].unique(), columns=['Watershed_ID'])

    uniqueIdDF.to_csv("WaterShedIDS-Pune.csv", index=False)
else:
    print("Failed")
