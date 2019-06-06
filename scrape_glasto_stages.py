import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


filepath = "glasto_stages_html.txt"

with open(filepath, "rb") as file:
    try:
        file_contents = file.read()
    except:
        print('Reading file failed')

soup = BeautifulSoup(file_contents, 'html.parser')

band_list = []

for stage in soup.findAll('div', attrs={'class':'box_header'}):
    if stage.find(class_='slabme'):
        continue
    else:
        val_stage = stage.find('h1').text
        for day in stage.findNext('table', attrs={'class':'lineup_table_group'}).findAll('table', attrs={'class':'lineup_table_day'}):
            val_day = day.find('h2').text
            day_bands = day.find('h2').parent
            counter = 0
            for band in day_bands.findAllNext('td'):
                if band.parent.parent != day:
                    break
                counter+=1
                if counter%2 != 0:
                    try:
                        val_band = band.find('a').text
                    except:
                        val_band = band.text
                else:
                    val_time = band.text
                    band_list.append([val_stage,val_day,val_band,val_time])

df_band_list = pd.DataFrame(band_list, columns = ['Stage','Day','Band','Time'])

df_band_list.to_csv('Glasto_stages_times.csv',index=False)
