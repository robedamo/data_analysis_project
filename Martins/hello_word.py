# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:19:19 2022

@author: Martina
"""
import pandas as pd
from sodapy import Socrata

#%%

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("analisi.transparenciacatalunya.cat", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(analisi.transparenciacatalunya.cat,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("vvp8-t2ai", limit=10000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#We have data from 2011. However we will only use 2020 and 2021 in order to 
#make it comparable with my companions data.

results_df=results_df.loc[(results_df['any']=='2020') | 
                          (results_df['any']=='2021') ]
                          

#All the strings ARE NOT in the same type of letter!
abps_serveis=results_df.servei_origen_dotaci.str.upper()


rp_c = "SERVEIS REGIONALS - RP CENTRAL"
rp_po="SERVEIS REGIONALS - RP PIRINEU OCCIDENTAL"
rp_g="SERVEIS REGIONALS - RP GIRONA"
rp_ms="SERVEIS REGIONALS - RP METROPOLITANA SUD"
rp_mn="SERVEIS REGIONALS - RP METROPOLITANA NORD"
rp_te="SERVEIS REGIONALS - RP TERRES DE L'EBRE"
rp_p="SERVEIS REGIONALS - RP PONENT"
rp_mb='SERVEIS REGIONALS - RP METROPOLITANA BARCELONA'

#All the string HAVE NOT the same format, so we have to change one by one:
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
We want to make a plot in which it will be represented the number of patrols
per abp.
"""

#First of all we have to make a mean of the number of patrols per abp along
#the years. We will do the same for the serveis.

#In order to do it, we create a list with the names of the ABP taking into 
#account that we have data segmentated in ABP and in Serveis

abps_list=[]
serveis_list=[]

for area in abps_serveis:
    
    if area.startswith('A'):
        if area in abps_list:
            0#print('Already in the list')
        else:
            abps_list.append(area)
    
    if area.startswith('S'):
        if area in serveis_list:
            0#print('Already in the list')
        else:
            serveis_list.append(area)

#%%
import numpy as np

#Now we collect the mean of the patrols in the different abps along the years.
#We do the same for the serveis

abp_mean_patrols_list=[]
serveis_mean_patrols_list=[]

for area in abps_list:
    specific_abp=results_df[abps_serveis== area]
    patrols_abp=specific_abp['mitjana_patrulles_di_ries']
    patrols_abp_list=patrols_abp.tolist()
    patrols_abp_list_int = [int(n) for n in patrols_abp_list]
    abp_mean_patrols=np.mean(patrols_abp_list_int)
    
    #It does not make sense having not a natural number of patrols, so we round 
    #them. At the same time, we add the number of the patrols on the list. 
    abp_mean_patrols_list.append(round(abp_mean_patrols))

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
#We plot the bar plot for the ABP
import matplotlib.pyplot as plt

plt.figure()
plt.bar(abps_list,abp_mean_patrols_list, 0.5)
plt.xticks(fontsize=8, rotation=90)
plt.yticks(fontsize=6)

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
plt.title('Mean daily patrols per RP (2020-2021)')
plt.bar(servei_list_plot[1:],serveis_mean_patrols_list[1:], 0.8, label='RP daily patrols')
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
plt.ylabel('Mean of daily patrols')
#We also plot the mean of the patrols along the years and considering all
#serveis regionals. We also round the number because we want a natural one.
print(round(np.mean(serveis_mean_patrols_list[1:])))
y=np.mean(serveis_mean_patrols_list[1:])
plt.axhline(y, ls = '--', color = 'red', label = 'Mean of daily patrols of all RP')
plt.legend()

#%%
#Now we will create a data frame with our data 
rp_df = pd.DataFrame(serveis_list_new[1:], columns =['RP'])
rp_df['daily patrols'] = pd.DataFrame(serveis_mean_patrols_list[1:])

#%%
# """
# Now we want to represent the mean number of daily patrols per inhabitant in 
# order to know if it is homogeneous
# """

# #First we import the data of the inhabitants for comarques and then we will
# #classify them for regions policials. 
# poblacio =  pd.read_excel('PoblacioRP.xlsx')

# rp_df_total=pd.DataFrame()

# rp_df_total=rp_df.merge(poblacio)

#%%
#Map

import geopandas as gpd

cat = gpd.read_file('C:/Users/Martina/projectADM/data_analysis_project/Robert/divisions-administratives-v2r1-municipis-1000000-20220801.shp', crs="EPSG:4326", encoding='utf-8'
                    )
f, ax = plt.subplots(figsize=(10,10))
cat.plot(ax = ax, color = "lightgray")

#%%DICTIONARY COMARQUES
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
               "RP GIRONA":RP_GIRONA, 'RP CENTRAL':RP_CENTRAL, "RP METROPOLITANA SUD":RP_METROPOLITANA_SUD,
               "RP CAMP DE TARRAGONA":RP_CAMP_DE_TARRAGONA, 
               "RP TERRES DE L'EBRE":RP_TERRES_DE_EBRE,"RP PONENT": RP_PONENT, 
               "RP PIRINEU OCCIDENTAL": RP_PIRINEU_OCCIDENTAL}
#check all the comarques are in the list except from Barcelonès
print('len', len(comarques))
for value in cat["NOMCOMAR"]:
    if value not in comarques :
        print(value)
        
#%%

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
#cat.insert(11, 'RP', com_list)
cat["RP"] = com_list
print(cat["NOMCOMAR"].value_counts())

new_map = cat[['RP','geometry']]
reg_poli = new_map.dissolve(by = 'RP')

#%% 
f, ax = plt.subplots(figsize=(10,10))
reg_poli.plot(ax = ax, color = "lightgray")
        


