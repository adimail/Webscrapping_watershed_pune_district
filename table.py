import re
from bs4 import BeautifulSoup
import requests
import html
import pandas as pd
import time

ids = pd.read_csv("WaterShedIDS-Pune.csv")

id_list = ids['Watershed_ID'].tolist()

data_list = []
count = 1

for id in id_list:
    start_time = time.time()

    url = f'https://slusi.dacnet.nic.in/dmwai/MAHARASHTRA/District/watershed/{
        id}.html'
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    coords = []

    for tag in soup.find_all():
        if 'coords' in tag.attrs:
            coords.append(tag['coords'])

    area_elements = soup.select('map[name="mapmap"] area')

    watershed_ids = [area['href'].split(
        '/')[-1].split('.')[0] for area in area_elements]

    onmouseover_elements = []

    individual_data_list = []

    for i, area in enumerate(area_elements):
        onmouseover_content = area.get('onmouseover')
        if onmouseover_content:
            content_inside_parentheses = html.unescape(onmouseover_content)

            table_data = BeautifulSoup(
                content_inside_parentheses, 'html.parser')

            area_value = table_data.find(
                'td', {'colspan': '2'}).text.split(':')[-1].strip()
            state = table_data.find('tr', {'bgcolor': '#BCF5A9'}).find_all('td')[
                1].text.strip()
            district = table_data.find('tr', {'bgcolor': '#F2F5A9'}).find_all('td')[
                1].text.strip()

            no_of_villages = ''
            village_tag = table_data.find('tr', {'bgcolor': '#F2F5A9'}).find(
                'b', string=lambda s: "Village" in s)
            if village_tag:
                for sibling in village_tag.find_next_siblings():
                    if sibling.name == 'b':
                        break
                    no_of_villages += str(sibling).strip()

            individual_data_list.append([watershed_ids[i],
                                        area_value, state, district, no_of_villages, coords[i], len(coords[i])])

    data_list += individual_data_list

    end_time = time.time()
    time_taken = end_time - start_time

    print(f"{id} Completed. Total sub watersheds: {len(individual_data_list)}\t{
          count}/41\t Time taken: {time_taken:.2f} seconds")

    count += 1

df = pd.DataFrame(data_list, columns=[
                  'Watershed_ID', 'Area', 'State(s)', 'District(s)', 'No. of Village(s)', 'Coords', 'Length of coords'])

print(df)
df.to_excel("Complete_Watersheds_in_Pune.xlsx")
