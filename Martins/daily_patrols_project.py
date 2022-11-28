# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:19:19 2022

@author: Martina
"""
import pandas as pd
from sodapy import Socrata

#%%

"""
DAILY PATROLS DATA CURATION
"""
#Import of data regarding daily patrols
client = Socrata("analisi.transparenciacatalunya.cat", None)
# First 10000 results, returned as JSON from API, converted to Python list of
# dictionaries by sodapy.
results = client.get("vvp8-t2ai", limit=10000)
# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#We have data from 2011. However we will only use 2020 and 2021.
results_df=results_df.loc[(results_df['any']=='2020') | 
                          (results_df['any']=='2021') ]
                          

#All the strings ARE NOT in the same type of letter. We put all data in majus.
abps_serveis=results_df.servei_origen_dotaci.str.upper()


rp_c = "SERVEIS REGIONALS - RP CENTRAL"
rp_po="SERVEIS REGIONALS - RP PIRINEU OCCIDENTAL"
rp_g="SERVEIS REGIONALS - RP GIRONA"
rp_ms="SERVEIS REGIONALS - RP METROPOLITANA SUD"
rp_mn="SERVEIS REGIONALS - RP METROPOLITANA NORD"
rp_te="SERVEIS REGIONALS - RP TERRES DE L'EBRE"
rp_p="SERVEIS REGIONALS - RP PONENT"
rp_mb='SERVEIS REGIONALS - RP METROPOLITANA BARCELONA'

#All the string HAVE NOT the same format, so we have to change them:
abps_serveis=(abps_serveis.replace('SERVEIS EGIONALS - RPCT', rp_c)
              .replace('SERVEIS REGIONALS - RPC', rp_c)
              .replace('SERVEIS REGIONALS - RPPO', rp_po)
              .replace('SERVEIS REGIONALS - RPG', rp_g)
              .replace('SERVEIS REGIONALS - RPMS', rp_ms)
              .replace('SERVEIS REGIONALS - RPMN', rp_mn)
              .replace('SERVEIS REGIONALS - RPTE', rp_te)
              .replace('SERVEIS REGIONALS - RPP', rp_p)
              .replace('SERVEIS REGIONALS - RPMB', rp_mb))
              

patrols=results_df['mitjana_patrulles_di_ries']

#%%

"""
BAR PLOT
"""

#First of all we have to make a mean of the number of patrols per RP along
#the years.

#In order to do it, we create a list with the names of the RP taking into 
#account that we have data segmentated in ABP and RP. 

serveis_list=[]

for area in abps_serveis:
    
    if area.startswith('S'):
        if area in serveis_list:
            0#print('Already in the list')
        else:
            serveis_list.append(area)

#%%
import numpy as np

#Now we collect the mean of the patrols in the different RP along the years.
serveis_mean_patrols_list=[]

for area in serveis_list:
    specific_servei=results_df[abps_serveis== area]
    patrols_serveis=specific_servei['mitjana_patrulles_di_ries']
    patrols_serveis_list=patrols_serveis.tolist()
    patrols_serveis_list_int = [int(n) for n in patrols_serveis_list]
    serveis_mean_patrols=np.mean(patrols_serveis_list_int)
    
#It does not make sense having not a natural number of patrols, so we round 
#them. At the same time, we add the number of the patrols on the list. 
    serveis_mean_patrols_list.append(round(serveis_mean_patrols))

#%%
#We plot the the bar plot for the Serveis Regionals
import matplotlib.pyplot as plt

#We delete the first part of the values of the list of Serveis Regionals in 
#order to do a clearer plot. 
serveis_list_new=[letter[20:] for letter in serveis_list]

#We write in two lines some Serveis Regionals in order to do a clear label
servei_list_plot=serveis_list_new.copy()
servei_list_plot[2]="RP TERRES\nDE L'EBRE"
servei_list_plot[4]="RP METROPOLITANA\nBARCELONA"
servei_list_plot[5]="RP PIRINEU\nOCCINDENTAL"
servei_list_plot[7]="RP CAMP DE\nTARRAGONA"
servei_list_plot[8]="RP METROPOLITANA\nSUD"
servei_list_plot[9]="RP METROPOLITANA\nNORD"


#We only ploy the Serveis Regionals
plt.figure()
plt.bar(servei_list_plot[1:],serveis_mean_patrols_list[1:], 0.8, label='Average daily patrols per RP')
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.ylabel('Daily patrols')
#We also plot the mean of the patrols along the years and considering all
#serveis regionals. We also round the number because we want a natural one.
print(round(np.mean(serveis_mean_patrols_list[1:])))
y=np.mean(serveis_mean_patrols_list[1:])
plt.axhline(y, ls = '--', color = 'red', label = 'Average daily patrols of all RP')
plt.legend(loc="upper left")

#%%
#Now we will create a data frame with our data 
rp_df = pd.DataFrame(serveis_list_new[1:], columns =['RP'])
rp_df['daily patrols'] = pd.DataFrame(serveis_mean_patrols_list[1:])

#%%

"""
MAP MAKING
"""

import geopandas as gpd

#We import the map of catalonia divided by comarques
cat = gpd.read_file('divisions-administratives-v2r1-municipis-1000000-20220801.shp', crs="EPSG:4326", encoding='utf-8'
                    )
f, ax = plt.subplots(figsize=(10,10))
cat.plot(ax = ax, color = "lightgray")

#We create a dictionary of the RP with its comarques
RP_METROPOLITANA_NORD = ["Maresme", 'Vallès Occidental', 'Vallès Oriental']
RP_GIRONA = ['Alt Empordà', 'Gironès', 'Selva', 'Garrotxa', 'Ripollès',
             "Pla de l'Estany", "Baix Empordà"]
RP_CENTRAL = ['Osona', 'Berguedà', 'Solsonès', 'Bages', 'Anoia', 'Moianès']
RP_METROPOLITANA_SUD = ['Baix Llobregat', 'Garraf', 'Alt Penedès']
RP_CAMP_DE_TARRAGONA = ['Baix Penedès', 'Alt Camp', 'Tarragonès', 'Conca de Barberà', 'Baix Camp','Priorat']
RP_TERRES_DE_EBRE = ["Ribera d'Ebre", "Terra Alta","Baix Ebre", "Montsià"]
RP_PONENT = ['Segrià', 'Garrigues', "Pla d'Urgell", "Urgell","Segarra", "Noguera"]
RP_PIRINEU_OCCIDENTAL = ["Pallars Jussà","Alt Urgell", "Pallars Sobirà", "Alta Ribagorça", "Val d'Aran", "Cerdanya"]

comarques = RP_METROPOLITANA_NORD + RP_GIRONA + RP_CENTRAL + RP_METROPOLITANA_SUD\
    + RP_CAMP_DE_TARRAGONA + RP_TERRES_DE_EBRE + RP_PONENT + RP_PIRINEU_OCCIDENTAL
    
comarq_dict = {'RP METROPOLITANA NORD':RP_METROPOLITANA_NORD, 
               "RP GIRONA":RP_GIRONA, 
               'RP CENTRAL':RP_CENTRAL, 
               "RP METROPOLITANA SUD":RP_METROPOLITANA_SUD,
               "RP CAMP DE TARRAGONA":RP_CAMP_DE_TARRAGONA, 
               "RP TERRES DE L'EBRE":RP_TERRES_DE_EBRE,
               "RP PONENT": RP_PONENT, 
               "RP PIRINEU OCCIDENTAL": RP_PIRINEU_OCCIDENTAL
               }

# generate a dictionary with the RP for each Comarca               
inverted_comarq_dict = {value:key for key in comarq_dict.keys() for value in comarq_dict[key]} 
      
#check all the comarques are in the list except from Barcelonès
print('len', len(comarques))
for value in cat["NOMCOMAR"]:
    if value not in comarques :
        print(value)
        
#%%

#We take into account that Barcelona has different municipis distributed in 
#different RP

com_list = []
ind = 0
print(len(cat["NOMCOMAR"]))
for comarca in cat["NOMCOMAR"]:
    for RP in comarq_dict.keys():
        if comarca in comarq_dict[RP]:
            com_list.append(RP)
            ind += 1
        elif comarca == 'Barcelonès':
            muni = cat["NOMMUNI"][ind]
            print(muni, ind, comarca)
            if muni != 'Barcelona':
                if muni == "l'Hospitalet de Llobregat":
                    com_list.append('RP METROPOLITANA SUD')
                else:
                    com_list.append('RP METROPOLITANA NORD')
                ind += 1
                break
            else:
                com_list.append('RP METROPOLITANA BARCELONA')
                ind += 1
                break
            
#%%
cat["RP"] = com_list
print(cat["NOMCOMAR"].value_counts())

new_map = cat[['RP','geometry']]
reg_poli = new_map.dissolve(by = 'RP')

# set RP as index of patrols df, to access data more easily    
rp_df = rp_df.set_index("RP")

# add a column to reg_poli, in which in each line there is the number of daily patrols of this line.
reg_poli["daily patrols"] = [rp_df.loc[rp, "daily patrols"] for rp in reg_poli.index]


#%%
"""
RP AREA DATA CURATION
"""

#### add a column for area per comarca, read from csv
areas_df = pd.read_csv("area_comarca.csv", skiprows=8, index_col=0)
areas_series = areas_df.Superficie
# now: align areas with RPs
print("Names of comarcas that are in area_comarca.csv, but not in comarques:", set(areas_series.index)-set(comarques))
print("Names of comarcas that are in comarques, but not in area_comarca.csv:", set(comarques)-set(areas_series.index))
areas_series = areas_series.rename(index={"Aran": "Val d'Aran"})
# drop provinces and entire Catalunya from series
areas_series = areas_series.drop("Cataluña").drop("Barcelona").drop("Lleida").drop("Tarragona").drop("Girona").drop("Barcelonès")
# add corresponding RP asa column
areas_RP_df = pd.DataFrame(areas_series)

#We have to add some cities in some RP because Barcelonés is divided in
#different RP
#The information has been taken from: 
#https://www.amb.cat/s/es/web/area-metropolitana/municipis-metropolitans.html

areas_RP_df.loc['Barcelona']=[100.3]
areas_RP_df.loc['Sant Adrià del Besos']=[3.8]
areas_RP_df.loc['Hospitalet de Llobregat']=[12.4]
areas_RP_df.loc['Badalona']=[21.2]
areas_RP_df.loc['Santa Coloma de Gramanet']=[7]

inverted_comarq_dict['Barcelona']='RP METROPOLITANA BARCELONA'
inverted_comarq_dict['Sant Adrià del Besos']='RP METROPOLITANA NORD'
inverted_comarq_dict['Hospitalet de Llobregat']='RP METROPOLITANA SUD'
inverted_comarq_dict['Badalona']='RP METROPOLITANA NORD'
inverted_comarq_dict['Santa Coloma de Gramanet']='RP METROPOLITANA NORD'

areas_RP_df["RP"] = [inverted_comarq_dict[com] for com in areas_RP_df.index]
rp_area_df = areas_RP_df.groupby("RP").sum()

# include the area data into the main gdf
reg_poli["daily patrols per area"] = [np.log(rp_df.loc[rp, "daily patrols"]/rp_area_df.loc[rp, "Superficie"]) for rp in reg_poli.index]
print(reg_poli)

#%%
"""
RP INHABITANTS DATA CURATION
"""
# add a column for population per RP, read from csv
pobl_df = pd.read_csv("pobl.csv", skiprows=0, index_col=0)
pobl_series = pobl_df.Població.drop("Total Catalunya").drop("Sense especificar")
pobl_series.index = "RP "+pobl_series.index.str.upper()
pobl_series = pobl_series.rename(index={'RP BARCELONA':'RP METROPOLITANA BARCELONA', 
                                         'RP TARRAGONA': 'RP CAMP DE TARRAGONA'})

pobl_df = pd.DataFrame(pobl_series)
# now: align areas with RPs
print("Names of comarcas that are in pobl.csv, but not in RP:", set(pobl_series.index)-set(comarq_dict.keys()))
print("Names of comarcas that are in RP, but not in pobl.csv:", set(comarq_dict.keys())-set(pobl_series.index))

# include the Population data into the main gdf
#We multiply by 1000 in order to have a large number beacuse the result would
#be too small in order to have sense

reg_poli["daily patrols per pobl"] = [rp_df.loc[rp, "daily patrols"]/pobl_df.loc[rp, "Població"]*100000 for rp in reg_poli.index]

print(reg_poli)

#%%
"""
MAP PLOTS
"""

#We create a new column in order to label better the RP in the map
reg_poli['RP_new']=['\n RP CAMP DE TARRAGONA', 'RP CENTRAL', 'RP GIRONA',
                    'RP METROPOLITANA BARCELONA', 'RP METROPOLITANA NORD', 
                    '\n\n RP METROPOLITANA SUD', 'RP PIRINEU OCCIDENTAL',
                    'RP PONENT', "RP TERRES DE L'EBRE"]

#1st map: Not normalized
# include the area data into the main gdf
f, ax = plt.subplots(figsize=(6,6))
reg_poli.plot(column='daily patrols', 
              ax=ax, 
              legend=True, 
              cmap="YlOrRd",
              legend_kwds={'label': "Average daily patrols"})


reg_poli = reg_poli.reset_index()

for index, row in reg_poli.iterrows():
    print(row)
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=8)
    plt.axis('off')

plt.show()

#%% 
#2nd map: Daily patrols per area
#plot with some adequate colormap (e.g. jet?), and label correctly
f, ax = plt.subplots(figsize=(6,6))
reg_poli.plot(column='daily patrols per area', 
              ax=ax, 
              legend=True, 
              cmap="YlOrRd",
              legend_kwds={'label': r"Logarithm of average daily patrols $km^2$"}) 
              

reg_poli = reg_poli.reset_index()

for index, row in reg_poli.iterrows():
    print(row)
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=8)
    plt.axis('off')

plt.show()

#%% 
#3rd map: Daily patrols per pobl 
#plot with some adequate colormap  and label correctly
f, ax = plt.subplots(figsize=(6,6))
reg_poli.plot(column='daily patrols per pobl', 
              ax=ax, 
              legend=True, 
              cmap="YlOrRd",
              legend_kwds={'label': "Average daily patrols per 100.000 inhabitants"}
              )


reg_poli = reg_poli.reset_index()

for index, row in reg_poli.iterrows():
    print(row)
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=8)
    plt.axis('off')

plt.show()
