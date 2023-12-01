import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://slusi.dacnet.nic.in/dmwai/MAHARASHTRA/District/PUNE.html"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    area_elements = soup.select('map[name="mapmap"] area')

    watershed_ids = [area['href'].split(
        '/')[-1].split('.')[0] for area in area_elements]

    images_folder_path = os.path.join(os.getcwd(), 'images')
    os.makedirs(images_folder_path, exist_ok=True)

    for watershed_id in watershed_ids:
        folder_path = os.path.join(images_folder_path, watershed_id)
        os.makedirs(folder_path, exist_ok=True)

        watershed_url = f"https://slusi.dacnet.nic.in/dmwai/MAHARASHTRA/District/watershed/{
            watershed_id}.html"
        watershed_response = requests.get(watershed_url)

        if watershed_response.status_code == 200:
            watershed_soup = BeautifulSoup(
                watershed_response.text, 'html.parser')
            micro_watershed_areas = watershed_soup.select(
                'map[name="mapmap"] area')

            for micro_watershed_area in micro_watershed_areas:
                micro_watershed_coords = micro_watershed_area['coords']
                micro_watershed_id = micro_watershed_area['href'].split(
                    '/')[-1].split('.')[0]

                micro_watershed_png_url = f"https://slusi.dacnet.nic.in/dmwai/MAHARASHTRA/District/watershed/microwatershed/{
                    micro_watershed_id}.png"
                micro_watershed_png_response = requests.get(
                    micro_watershed_png_url)

                if micro_watershed_png_response.status_code == 200:
                    png_file_path = os.path.join(
                        folder_path, f"{micro_watershed_id}.png")

                    with open(png_file_path, 'wb') as png_file:
                        png_file.write(micro_watershed_png_response.content)

                    print(f"Downloaded: {png_file_path}")
                else:
                    print(
                        f"Failed to download PNG for micro-watershed {micro_watershed_id}")

        else:
            print(f"Failed to retrieve micro-watershed page for {
                  watershed_id}. Status code: {watershed_response.status_code}")

    print("Download process completed.")
else:
    print(f"Failed to retrieve the main page. Status code: {
          response.status_code}")
