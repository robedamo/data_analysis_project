# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:24:52 2022

@author: rober
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("analisi.transparenciacatalunya.cat", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(analisi.transparenciacatalunya.cat,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("bp4b-qsst", limit = 10000)
# Convert to pandas DataFrame
disap_data = pd.DataFrame.from_records(results)
disap_data["edat"] = disap_data["edat"].astype('int')
x = np.linspace(0,100,21)
# plt.figure()
# plt.hist(disap_data["edat"],density=False, 
#                         bins = x)
# plt.xlabel('Age (yrs)')
# plt.show()


mc = disap_data.loc[disap_data["sexe"]=='Dona']["edat"].reset_index()
fm = disap_data.loc[disap_data["sexe"]=='Home']["edat"].reset_index()
#data frame for each gender, disappearences per age
ages = np.linspace(0,100, 101)
age_df = pd.DataFrame(columns = ["Age", "Male" , "Female"])
for age in ages:
    new_df = pd.DataFrame([{"Age":age,"Male":mc[mc.edat == age].shape[0],"Female":fm[fm.edat == age].shape[0]}])
    age_df = pd.concat([age_df, new_df], axis=0, ignore_index=True)
    
age_df = age_df.set_index("Age")
#%%

age_df.plot(kind='bar',ylabel ='Disappearences per year', xlabel = 'Ages(years)', stacked=False, color=['skyblue', 'red'])
#%%
plt.figure()
plt.xlabel('Age (years)')
plt.xticks(x)
plt.ylabel('Disappearences per 5 years')
labels1 = ["Male", "Female"]
sns.histplot(disap_data["edat"],bins = x, kde =True, color = 'blue', multiple="stack")
plt.legend()
plt.show()
#%%

plt.pie(disap_data["sexe"].value_counts())
plt.legend(labels1)
#%%

print(disap_data.loc[disap_data["sexe"]=='Home'])

#%%
import geopandas as gpd

cat = gpd.read_file('C:/Users/rober/OneDrive/Documents/master/dades_massives/data_analysis_project/Robert/divisions-administratives-v2r1-municipis-1000000-20220801.shp', crs="EPSG:4326")
f, ax = plt.subplots(figsize=(10,10))
cat.plot(ax = ax, color = "lightgray")

#%%
RP_METROPOLITANA_NORD = ["Maresme", 'Vallès Occidental', 'Vallès Oriental']
RP_GIRONA = ['Alt Empordà', 'Gironès', 'Selva', 'Garrotxa', 'Ripollès',
             "Pla de l'Estany", "Baix Empordà"]
RP_CENTRAL = ['Osona', 'Berguedà', 'Solsonès', 'Bages', 'Anoia', 'Moianès']
RP_METROPOLITANA_SUD = ['Baix Llobregat', 'Garraf', 'Alt Penedès']
RP_CAMP_DE_TARRAGONA = ['Baix Penedès', 'Alt Camp', 'Tarragonès', 'Conca de Barberà', 'Baix Camp','Priorat']
RP_TERRES_DE_EBRE = ["Ribera d'Ebre", "Terra Alta","Baix Ebre", "Montsià"]
RP_PONENT = ['Segrià', 'Garrigiues', "Pla d'Urgell", "Urgell","Segarra", "Noguera"]
RP_PIRINEU_OCCIDENTAL = ["Pallars Jussà","Alt Urgell", "Pallars Sobirà", "Alta Ribagorça", "Val d'Aran"]

comarq_dict = {'RP METROPOLITANA NORD':RP_METROPOLITANA_NORD, 
               "RP GIRONA":RP_GIRONA, "RP METROPOLITANA SUD":RP_METROPOLITANA_SUD,
               "RP CAMP DE TARRAGONA":RP_CAMP_DE_TARRAGONA, 
               "RP TERRES DE L'EBRE":RP_TERRES_DE_EBRE,"RP PONENT": RP_PONENT, 
               "RP PIRINEU OCCIDENTAL": RP_PIRINEU_OCCIDENTAL}

for value in cat["NOMCOMAR"].value_counts():
    print(value in cat["NOMCOMAR"])

com_list = []
for comarca in cat["NOMCOMAR"]:
    for key in comarq_dict.keys():
        if comarca in comarq_dict[key]:
            com_list.append(key)
print(com_list)

print(cat["NOMCOMAR"].value_counts())
print(disap_data["regi_policial"].value_counts())
