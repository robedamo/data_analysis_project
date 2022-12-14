# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:24:52 2022

@author: rober
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

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

#converting age to ints

disap_data["edat"] = disap_data["edat"].astype('int')

x = np.linspace(0,100,21)

#creating a dataframe with disappearances by age and gender
mc = disap_data.loc[disap_data["sexe"]=='Dona']["edat"].reset_index()
fm = disap_data.loc[disap_data["sexe"]=='Home']["edat"].reset_index()
ages = np.linspace(1,100, 100)

age_df = pd.DataFrame(columns = ["Age", "Male" , "Female"])
for age in ages:
    new_df = pd.DataFrame([{"Age":int(age),"Male":mc[mc.edat == age].shape[0],"Female":fm[fm.edat == age].shape[0]}])
    age_df = pd.concat([age_df, new_df], axis=0, ignore_index=True)
    
age_df = age_df.set_index("Age")

#calculating total adult disappearances by gender
dis_adult_m = 0
dis_adult_w = 0

for age in range(18,61):
    dis_adult_m += age_df.loc[age]["Male"]
    dis_adult_w += age_df.loc[age]["Female"]
    
print("Adult male missing = ", dis_adult_m, "Adult female missing =", dis_adult_w)
#%% BAR PLOT AGE GROUPED BY 2 YEARS
counts = 2

age_l_m = []
age_l_f = []
#from the dataframe we created for each age, we create anotherone that has 2  
#consecutive ages in each row

# generate male col
for age in range(0,99,2):
    pair = age_df["Male"].iloc[age]
    pair += age_df["Male"].iloc[age+1]
    age_l_m.append(pair)

#generate female col
for age in range(0,99,2):
    pair = age_df["Female"].iloc[age]
    pair += age_df["Female"].iloc[age+1]
    age_l_f.append(pair)

#create df

age_df2 = pd.DataFrame(columns = ["Age", "Male" , "Female"])

for i in range(0,50):
    new_df = pd.DataFrame([{"Age":str(counts-2)+'-'+str(counts),"Male":age_l_m[i],"Female":age_l_f[i]}])
    age_df2 = pd.concat([age_df2, new_df], axis=0, ignore_index=True)
    counts += 2
age_df2 = age_df2.set_index("Age")
#%% PLOT BAR PLOT grouped by 2 yrs
f, ax = plt.subplots(figsize = (14,10))
ax.set_xlabel('Ages(years)',fontsize = 18)
ax.set_ylabel('Disappearances per 2 years', fontsize = 18)
age_df2.plot(ax = ax, kind='bar',
             width = 0.8,
             stacked=False, 
             xlabel = "Age (years)",
             color=['skyblue', 'red'],
             fontsize = 17)
plt.legend(["Male", "Female"], prop={'size': 16})
#%%  every 5 years
plt.figure()
plt.xlabel('Age (years)')
plt.xticks(x)
plt.ylabel('Disappearences per 5 years')
labels1 = ["Male", "Female"]
sns.histplot(disap_data["edat"],bins = x, kde =True, color = 'blue', multiple="stack")
plt.legend()
plt.show()
#%% PIE chart
labels1 = ["Male", "Female"]
plt.pie(disap_data["sexe"].value_counts(),
        wedgeprops=dict(width=0.5),
        autopct='%1.0f%%')
plt.legend(labels1)

print(disap_data.loc[disap_data["sexe"]=='Home'])

#%% MAPS, GEOPANDAS
import geopandas as gpd

cat = gpd.read_file('C:/Users/rober/OneDrive/Documents/master/dades_massives/data_analysis_project/Robert/divisions-administratives-v2r1-municipis-1000000-20220801.shp', crs="EPSG:4326")
f, ax = plt.subplots(figsize=(10,10))
#cat.plot(ax = ax, color = "lightgray")

#%%DICTIONARY COMARQUES

#we create a dict wit {RP1:[comarques in RP1], ...}

RP_METROPOLITANA_NORD = ["Maresme", 'Vall??s Occidental', 'Vall??s Oriental']
RP_GIRONA = ['Alt Empord??', 'Giron??s', 'Selva', 'Garrotxa', 'Ripoll??s',
             "Pla de l'Estany", "Baix Empord??"]
RP_CENTRAL = ['Osona', 'Bergued??', 'Solson??s', 'Bages', 'Anoia', 'Moian??s']
RP_METROPOLITANA_SUD = ['Baix Llobregat', 'Garraf', 'Alt Pened??s']
RP_CAMP_DE_TARRAGONA = ['Baix Pened??s', 'Alt Camp', 'Tarragon??s', 'Conca de Barber??', 'Baix Camp','Priorat']
RP_TERRES_DE_EBRE = ["Ribera d'Ebre", "Terra Alta","Baix Ebre", "Montsi??"]
RP_PONENT = ['Segri??', 'Garrigues', "Pla d'Urgell", "Urgell","Segarra", "Noguera"]
RP_PIRINEU_OCCIDENTAL = ["Pallars Juss??","Alt Urgell", "Pallars Sobir??", "Alta Ribagor??a", "Val d'Aran", "Cerdanya"]

#list with all comarques

comarques = RP_METROPOLITANA_NORD + RP_GIRONA + RP_CENTRAL + RP_METROPOLITANA_SUD\
    + RP_CAMP_DE_TARRAGONA + RP_TERRES_DE_EBRE + RP_PONENT + RP_PIRINEU_OCCIDENTAL

#dictionary of comarques sorted by RP
comarq_dict = {'RP METROPOLITANA NORD':RP_METROPOLITANA_NORD, 
               "RP GIRONA":RP_GIRONA, 'RP CENTRAL':RP_CENTRAL, "RP METROPOLITANA SUD":RP_METROPOLITANA_SUD,
               "RP CAMP DE TARRAGONA":RP_CAMP_DE_TARRAGONA, 
               "RP TERRES DE L'EBRE":RP_TERRES_DE_EBRE,"RP PONENT": RP_PONENT, 
               "RP PIRINEU OCCIDENTAL": RP_PIRINEU_OCCIDENTAL}

#check all the comarques are in the list except from Barcelon??s
print('len', len(comarques))
for value in cat["NOMCOMAR"]:
    if value not in comarques :
        print(value)

#we will add a row to the original geopandas dataframe with the RPs
com_list = []
ind = 0
print(len(cat["NOMCOMAR"]))
for comarca in cat["NOMCOMAR"]:
    for RP in comarq_dict.keys():
        if comarca in comarq_dict[RP]:
            com_list.append(RP)
            ind += 1
        elif comarca == 'Barcelon??s':
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
cat.insert(11, 'RP', com_list) #Activate in 1st run
cat["RP"] = com_list
print(cat["NOMCOMAR"].value_counts())
print(disap_data["regi_policial"].value_counts())
#%% NEW RP MAP

new_map = cat[['RP','geometry']]
reg_poli = new_map.dissolve(by = 'RP', as_index = True)#dissolving by RP so we 
#get the polygons we are interested in
#reg_poli = reg_poli.set_index("RP")
reg_poli.insert(1, 'DISAP', disap_data["regi_policial"].value_counts())
#%% 
#dict of population in each RP
RP_tot_pop = {'RP METROPOLITANA NORD':2195758, 
               "RP GIRONA":766681, 'RP CENTRAL':530715, "RP METROPOLITANA SUD":1366442,
               "RP CAMP DE TARRAGONA":637198, 
               "RP TERRES DE L'EBRE":179574,"RP PONENT":367016, 
               "RP PIRINEU OCCIDENTAL": 72913, "RP METROPOLITANA BARCELONA":1664182}
#putting the numbers in the gpd df
for key in RP_tot_pop.keys():
    print(reg_poli.at[key, "DISAP"]/RP_tot_pop[key])
    reg_poli.at[key, "DISAP"] = reg_poli.at[key, "DISAP"]#*100000/RP_tot_pop[key]

#new row for the labels
reg_poli['RP_new']=['\n RP CAMP DE TARRAGONA', 'RP CENTRAL', 'RP GIRONA',
                    'RP METROPOLITANA BARCELONA', 'RP METROPOLITANA NORD', 
                    '\n\n RP METROPOLITANA SUD', 'RP PIRINEU OCCIDENTAL',
                    'RP PONENT', "RP TERRES DE L'EBRE"]
#%% PLOTTING MAP
min_val, max_val = 0.1,1.0
n = 100
f, ax = plt.subplots(figsize=(10,10))
vmin = reg_poli.DISAP.min()
vmax = reg_poli.DISAP.max()
orig_cmap = plt.cm.YlOrRd
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
reg_poli.plot(ax = ax, column='DISAP', cmap=cmap, label = "a", legend=False)
cbar = f.colorbar(sm)
cbar.set_label('Disappearances per 100.000 inhabitants', fontsize = 15)
cbar.ax.tick_params(labelsize=15)
plt.axis('off')

reg_poli = reg_poli.reset_index()

for index, row in reg_poli.iterrows():
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=8)
    plt.axis('off')
#plt.title('Disappearances in Catalonia per 100.000 inhabitants', fontsize = 18)
plt.show()


#%% NOT NORMALIZED
min_val, max_val = 0.1,1.0
n = 100
f, ax = plt.subplots(figsize=(10,10))
vmin = reg_poli.DISAP.min()
vmax = reg_poli.DISAP.max()
orig_cmap = plt.cm.YlOrRd
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
reg_poli.plot(ax = ax, column='DISAP', cmap=cmap, label = "a", legend=False)

reg_poli = reg_poli.reset_index()

for index, row in reg_poli.iterrows():
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=8)
    plt.axis('off')
    
cbar = f.colorbar(sm)
cbar.set_label('Total Disappearances', fontsize = 15)
cbar.ax.tick_params(labelsize=15)
plt.axis('off')
#plt.title('Disappearances in Catalonia', fontsize = 18)
plt.show()