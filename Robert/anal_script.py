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
ages = np.linspace(1,100, 100)
age_df = pd.DataFrame(columns = ["Age", "Male" , "Female"])
for age in ages:
    new_df = pd.DataFrame([{"Age":int(age),"Male":mc[mc.edat == age].shape[0],"Female":fm[fm.edat == age].shape[0]}])
    age_df = pd.concat([age_df, new_df], axis=0, ignore_index=True)
    
age_df = age_df.set_index("Age")
#%% BAR PLOT AGE GROUPED BY 2
counts = 2

age_l_m = []
age_l_f = []
for age in range(0,99,2):
    pair = age_df["Male"].iloc[age]
    pair += age_df["Male"].iloc[age+1]
    age_l_m.append(pair)

for age in range(0,99,2):
    pair = age_df["Female"].iloc[age]
    pair += age_df["Female"].iloc[age+1]
    age_l_f.append(pair)
    
age_df2 = pd.DataFrame(columns = ["Age", "Male" , "Female"])

for i in range(0,50):
    new_df = pd.DataFrame([{"Age":str(counts-2)+'-'+str(counts),"Male":age_l_m[i],"Female":age_l_f[i]}])
    age_df2 = pd.concat([age_df2, new_df], axis=0, ignore_index=True)
    counts += 2
age_df2 = age_df2.set_index("Age")
#%% PLOT BAR PLOT
age_df2.plot(kind='bar',ylabel ='Disappearences per year', xlabel = 'Ages(years)', stacked=False, color=['skyblue', 'red'])
#%% HISTO
plt.figure()
plt.xlabel('Age (years)')
plt.xticks(x)
plt.ylabel('Disappearences per 5 years')
labels1 = ["Male", "Female"]
sns.histplot(disap_data["edat"],bins = x, kde =True, color = 'blue', multiple="stack")
plt.legend()
plt.show()
#%% PIE

plt.pie(disap_data["sexe"].value_counts())
plt.legend(labels1)
#%%

print(disap_data.loc[disap_data["sexe"]=='Home'])

#%% MAPS, GEOPANDAS
import geopandas as gpd

cat = gpd.read_file('C:/Users/rober/OneDrive/Documents/master/dades_massives/data_analysis_project/Robert/divisions-administratives-v2r1-municipis-1000000-20220801.shp', crs="EPSG:4326")
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
print(disap_data["regi_policial"].value_counts())
#%%RP MAPA

new_map = cat[['RP','geometry']]
reg_poli = new_map.dissolve(by = 'RP')
reg_poli.insert(1, 'DISAP', disap_data["regi_policial"].value_counts())
#%% 
import matplotlib
RP_tot_pop = {'RP METROPOLITANA NORD':2195758, 
               "RP GIRONA":766681, 'RP CENTRAL':530715, "RP METROPOLITANA SUD":1366442,
               "RP CAMP DE TARRAGONA":637198, 
               "RP TERRES DE L'EBRE":179574,"RP PONENT":367016, 
               "RP PIRINEU OCCIDENTAL": 72913, "RP METROPOLITANA BARCELONA":1664182}
#reg_poli.set_index("RP")
for key in RP_tot_pop.keys():
    print(reg_poli.at[key, "DISAP"]/RP_tot_pop[key])
    reg_poli.at[key, "DISAP"] = reg_poli.at[key, "DISAP"]*10000/RP_tot_pop[key]
min_val, max_val = 0.3,1.0
#%%
n = 100
f, ax = plt.subplots(figsize=(10,10))
vmin = reg_poli.DISAP.min()
vmax = reg_poli.DISAP.max()
orig_cmap = plt.cm.Reds
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
#sm = plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.LogNorm(vmin=vmin, vmax=vmax))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
reg_poli.plot(ax = ax, column='DISAP', cmap=cmap, label = "a", legend=False)
cbar = f.colorbar(sm)
cbar.set_label('Disappearences', fontsize = 12)
plt.axis('off')
plt.title('Disappearences in each RP in Catalonia per 10000 inhabitants', fontsize = 15)
plt.show()
