#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:25:48 2022

@author: nilmasocastro
"""

import pandas as pd
import matplotlib.pyplot as plt
from sodapy import Socrata
import numpy as np
import geopandas as gpd
import datetime
import matplotlib

#%%
#Obtain the data using the API

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("analisi.transparenciacatalunya.cat", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(analisi.transparenciacatalunya.cat,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 8000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("qxev-y8x7", limit=7923)

#%%
# Convert to pandas DataFrame
data_df = pd.DataFrame.from_records(results)

#%%
# We remove the data of 2022 (since there is only 3 values of different RP and ABP (not correlated))
data_df = data_df.set_index('any')
data_df = data_df.drop('2022')
data_df = data_df.reset_index()

# Also erase the 'Divisió de Transport' RP since it has not analysis value
data_df = data_df.set_index('regi_policial_rp')
data_df = data_df.drop('Divisió de Transport')
data_df = data_df.reset_index()


# Since there is 2 RP Metropolitana Nord we need to change the name of these strings
data_df = data_df.replace('RP  Metropolitana Nord', 'RP Metropolitana Nord')
# replace finds all 'RP  Metropolitana Nord' in the dataframe and substitutes with
# 'RP Metropolitana Nord' (only one blankspace between 'RP and Metropolitana')

print(data_df['regi_policial_rp'].value_counts())
# There are more values for RP Metropolitana Nord since there are more ABPs in it


#We need to change the number of visits to a integer, since now is considered an string
data_df['nombre_de_visites'] = data_df['nombre_de_visites'].astype('int')


# We also need to transform the data of time into seconds to work easier
times_df = data_df[['mitjana_temps_espera']].copy()
times_df['mitjana_temps_espera'] = pd.to_datetime(times_df['mitjana_temps_espera'])

# We write the time in minutes (with decimals representing the seconds)
times_df['mitjana_temps_espera'] = times_df.mitjana_temps_espera.dt.hour * 60 + \
                                   times_df.mitjana_temps_espera.dt.minute + \
                                   times_df.mitjana_temps_espera.dt.second / 60
data_df['mitjana_temps_espera'] = times_df['mitjana_temps_espera']

number_of_years = 10 # to divide and obtain the mean for all years (from 2011 to 2021)


#%%
# Specific ABP
ABP = 'Granollers'
single_ABP = data_df[data_df['rea_b_sica_policial_abp'] == 'ABP ' + ABP]

mes_visites = pd.DataFrame({'Any':single_ABP.loc[:,'any'], 'Nombre visites':single_ABP.loc[:,'nombre_de_visites']})
mes_visites = mes_visites.set_index('Any')

xticks_list = np.empty(number_of_years*12, dtype=tuple)
xticks_list = xticks_list.tolist()

for i in range(0,number_of_years*12):
    if (i % 12) == 0:
        xticks_list.insert(i,tuple(2011+i//12))
    else:
        xticks_list.insert(i,'')

# To plot the number of visits in one specific ABP
mes_visites.plot(kind='bar', title='ABP '+ABP, xticks=(), xlabel='Year', ylabel='Number of visits', 
                 rot=60, stacked=False, legend=False)



#%%
# We want to plot the number of visits in every RP from 2011 to 2021

# We create a DataFrame with 2 columns with the RP and number of visits
visites_RP = data_df[['regi_policial_rp','nombre_de_visites']].copy()


#new_df = data_df[['regi_policial_rp','nombre_de_visites','any']].copy()

#new_df = new_df[new_df['any'] > '2019']

#visites_RP = new_df.copy()



# Write all the RPs in a list
list_RP = [i for i in (visites_RP['regi_policial_rp'].value_counts()).index]

mean_visites_RP = []
visites_RP = visites_RP.set_index('regi_policial_rp')

for RP in list_RP:
    specific_RP = visites_RP.loc[RP]
    # Compute the mean for all RPs, round the number and append into the list
    #mean_visites_RP.append(np.round(sum(specific_RP.nombre_de_visites)/number_of_years, decimals=0))
    mean_visites_RP.append(np.round(sum(specific_RP.nombre_de_visites)/2, decimals=0))

mean_visites_RP = [int(i) for i in mean_visites_RP] #transform the mean visits into integers

# Create a new DataFrame in order to plot
mean_visites_RP = pd.DataFrame(data=mean_visites_RP, index=list_RP, columns=['Mean number of visits'])

#%%

# Plot the average number of visits per year for every RP

mean_visites_RP.plot(kind='bar', ylabel='Average number fo visits per year', 
                     rot=90, legend=False, stacked=True)
plt.tight_layout()
plt.savefig('number_visits_RP.png')

visites_RP = visites_RP.reset_index()

#%%
# We want to plot the average time that takes to be attended after entering the police department.
# We need to sum all times and divide by the size of the sample (depends on the RP, since
# every RP has different number of ABP).
time_RP = data_df[['regi_policial_rp','mitjana_temps_espera']].copy()

mean_time_RP = []
time_RP = time_RP.set_index('regi_policial_rp')

for RP in list_RP:
    specific_RP = time_RP.loc[RP]
    # Compute the mean for all RPs and append into the list
    mean_time_RP.append(sum(specific_RP.mitjana_temps_espera)/len(specific_RP))

mean_time_RP = pd.DataFrame(data=mean_time_RP, index=list_RP, columns=['Mean waiting time'])


#%%
# Plot the average number of visits per year for every RP
mean_time_RP.plot(kind='bar', ylabel='Average waiting time (min)', 
                     rot=90, legend=False)

y = np.mean(time_RP.mitjana_temps_espera)
plt.axhline(y, ls = '--', color = 'red')
plt.text(3, 16, 'Mean', fontsize=10, color='red')
plt.tight_layout()
plt.savefig('waiting_time_RP.png')


time_RP = time_RP.reset_index()



#%%
# We want to plot two maps of the RP for the mean visits in a year and the average
# time of being attended. This is done using geopandas.

#cat = gpd.read_file('/Users/nilmasocastro/Desktop/MSc/Subjects/Data_analysis/group_repository/data_analysis_project/Nil/divisions-administratives-v2r1-municipis-1000000-20220801.shp', crs="EPSG:4326")
cat = gpd.read_file('divisions-administratives-v2r1-municipis-1000000-20220801.shp', crs="EPSG:4326")

#%% DICTIONARY COMARQUES
RP_METROPOLITANA_NORD = ["Maresme", 'Vallès Occidental', 'Vallès Oriental']
RP_GIRONA = ['Alt Empordà', 'Gironès', 'Selva', 'Garrotxa', 'Ripollès',
             "Pla de l'Estany", "Baix Empordà"]
RP_CENTRAL = ['Osona', 'Berguedà', 'Solsonès', 'Bages', 'Anoia', 'Moianès']
RP_METROPOLITANA_SUD = ['Baix Llobregat', 'Garraf', 'Alt Penedès']
RP_CAMP_DE_TARRAGONA = ['Baix Penedès', 'Alt Camp', 'Tarragonès', 'Conca de Barberà', 'Baix Camp','Priorat']
RP_TERRES_DE_EBRE = ["Ribera d'Ebre", "Terra Alta","Baix Ebre", "Montsià"]
RP_PONENT = ['Segrià', 'Garrigues', "Pla d'Urgell", "Urgell","Segarra", "Noguera"]
RP_PIRINEU_OCCIDENTAL = ["Pallars Jussà","Alt Urgell", "Pallars Sobirà", "Alta Ribagorça", "Val d'Aran", "Cerdanya"]

# list with all comarques
comarques = RP_METROPOLITANA_NORD + RP_GIRONA + RP_CENTRAL + RP_METROPOLITANA_SUD\
    + RP_CAMP_DE_TARRAGONA + RP_TERRES_DE_EBRE + RP_PONENT + RP_PIRINEU_OCCIDENTAL

# dictionary of comarques sorted by RP
comarq_dict = {'RP Metropolitana Nord':RP_METROPOLITANA_NORD, 
               'RP Girona':RP_GIRONA, 'RP Central':RP_CENTRAL, 'RP Metropolitana Sud':RP_METROPOLITANA_SUD,
               'RP Camp de Tarragona':RP_CAMP_DE_TARRAGONA, 
               "RP Terres de l'Ebre":RP_TERRES_DE_EBRE,'RP Ponent': RP_PONENT, 
               'RP Pirineu Occidental': RP_PIRINEU_OCCIDENTAL}

#%%
# we will add a column to the original geopandas dataframe with the RPs
com_list = []
ind = 0

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
                    com_list.append('RP Metropolitana Sud')
                else:
                    com_list.append('RP Metropolitana Nord')
                ind += 1
                break
            else:
                com_list.append('RP Metropolitana Barcelona')
                ind += 1
                break

cat['RP'] = com_list # we add a new column with every RP

# We create a new dataframe with the data to plot
map_regi = cat[['RP','geometry']]
map_regi = map_regi.dissolve(by = 'RP')

map_regi['Mean number of visits'] = 0 # we create a new blank column
map_regi['Mean waiting time'] = 0

#%%
# we write our data into this map_regi geopandas dataframe
for RP in list_RP:
    map_regi.loc[RP,'Mean number of visits'] = mean_visites_RP.loc[RP,'Mean number of visits']
    map_regi.loc[RP,'Mean waiting time'] = mean_time_RP.loc[RP,'Mean waiting time']
    
#%%
"""
MAP PLOTS
"""

map_regi['RP_new']=['\n RP CAMP DE TARRAGONA', 'RP CENTRAL', 'RP GIRONA',
                    'RP METROPOLITANA BARCELONA', 'RP METROPOLITANA NORD', 
                    '\n\n RP METROPOLITANA SUD', 'RP PIRINEU OCCIDENTAL',
                    'RP PONENT', "RP TERRES DE L'EBRE"]

#%% PLOT FOR AVERAGE NUMBER OF VISITS PER YEAR IN EACH RP

f, ax = plt.subplots(figsize=(8,8))
cat.plot(ax = ax, color = "lightgray")


plt.title('Average number of visits per year in each RP', fontsize=13)
plt.axis(False)

min_val, max_val = 0.1,1.0
n = 100
vmin = map_regi['Mean number of visits'].min()
vmax = map_regi['Mean number of visits'].max()
orig_cmap = plt.cm.Reds
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
cbar = f.colorbar(sm)
cbar.set_label('Mean number of visits per year', fontsize = 12)
cbar.ax.tick_params(labelsize=12)
plt.tight_layout()

map_regi.plot(ax = ax, column='Mean number of visits', cmap=cmap)

f.savefig('cat_visits.png')
plt.show()


#%% FOR GROUP PRESENTATION
f, ax = plt.subplots(figsize=(10,10))
map_regi.plot(column='Mean number of visits', 
              ax=ax, 
              legend=True, 
              cmap="YlOrRd",
              legend_kwds={'label': "Average number of visits"})


map_regi = map_regi.reset_index()

for index, row in map_regi.iterrows():
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=9)
    plt.axis(False)

f.savefig('cat_visits_yorld.png')
plt.show()

#%% PLOT FOR AVERAGE WAITING TIME IN EACH RP

f, ax = plt.subplots(figsize=(8,8))
cat.plot(ax = ax, color = "lightgray")


plt.title('Average waiting time in each RP', fontsize=13)
plt.axis(False)

min_val, max_val = 0.1,1.0
n = 100
vmin = map_regi['Mean waiting time'].min()
vmax = map_regi['Mean waiting time'].max()
orig_cmap = plt.cm.Reds
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
cbar = f.colorbar(sm)
cbar.set_label('Mean waiting time (min)', fontsize = 12)
cbar.ax.tick_params(labelsize=12)
plt.tight_layout()

map_regi.plot(ax = ax, column='Mean waiting time', cmap=cmap)

f.savefig('cat_time.png')
plt.show()

#%% FOR GROUP PRESENTATION
f, ax = plt.subplots(figsize=(10,10))
map_regi.plot(column='Mean waiting time', 
              ax=ax, 
              legend=True, 
              cmap="YlOrRd",
              legend_kwds={'label': "Average waiting time (min)"})


map_regi = map_regi.reset_index()

for index, row in map_regi.iterrows():
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=9)
    plt.axis(False)

f.savefig('cat_time_yorld.png')
plt.show()

#%% DENSITY per 100000 habitants

RP_tot_pop = {'RP Metropolitana Nord':2195758, 
               "RP Girona":766681, 'RP Central':530715, "RP Metropolitana Sud":1366442,
               "RP Camp de Tarragona":637198, 
               "RP Terres de l'Ebre":179574,"RP Ponent":367016, 
               "RP Pirineu Occidental": 72913, "RP Metropolitana Barcelona":1664182}

map_regi['Mean number of visits 100000'] = 0
map_regi['Mean waiting time 100000'] = 0

for key in RP_tot_pop.keys():
    map_regi.at[key, "Mean number of visits 100000"] = map_regi.at[key, "Mean number of visits"]*100000/RP_tot_pop[key]
    map_regi.at[key, "Mean waiting time 100000"] = map_regi.at[key, "Mean waiting time"]*100000/RP_tot_pop[key]
    
#%% PLOT FOR AVERAGE NUMBER OF VISITS PER YEAR IN EACH RP FOR 100000 HABITANTS

f, ax = plt.subplots(figsize=(8,8))
cat.plot(ax = ax, color = "lightgray")


plt.title('Average number of visits per year in each RP for 100000 habitants', fontsize=13)
plt.axis(False)

min_val, max_val = 0.1,1.0
n = 100
vmin = map_regi['Mean number of visits 100000'].min()
vmax = map_regi['Mean number of visits 100000'].max()
orig_cmap = plt.cm.Reds
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
cbar = f.colorbar(sm)
cbar.set_label('Mean number of visits per year per 100000', fontsize = 12)
cbar.ax.tick_params(labelsize=12)
plt.tight_layout()

map_regi.plot(ax = ax, column='Mean number of visits 100000', cmap=cmap)

f.savefig('cat_visits_100000.png')
plt.show()

#%% PLOT PRESENTATION

f, ax = plt.subplots(figsize=(10,10))
map_regi.plot(column='Mean number of visits 100000', 
              ax=ax, 
              legend=True, 
              cmap="YlOrRd",
              legend_kwds={'label': "Average number of visits per 100.000 inhabitants"})


map_regi = map_regi.reset_index()

for index, row in map_regi.iterrows():
    print(row)
    xy = row['geometry'].centroid.coords[:]
    xytext = row['geometry'].centroid.coords[:]
    plt.annotate(row['RP_new'], xy=xy[0], xytext=xytext[0], horizontalalignment='center', verticalalignment='center', fontsize=9)
    plt.axis(False)

f.savefig('cat_visits_100000_yorld.png')
plt.show()

#%% PLOT FOR AVERAGE WAITING TIME IN EACH RP FOR 100000 HABITANTS

f, ax = plt.subplots(figsize=(8,8))
cat.plot(ax = ax, color = "lightgray")


plt.title('Average waiting time in each RP for 100000 habitants', fontsize=13)
plt.axis(False)

min_val, max_val = 0.1,1.0
n = 100
vmin = map_regi['Mean waiting time'].min()
vmax = map_regi['Mean waiting time'].max()
orig_cmap = plt.cm.Reds
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
cbar = f.colorbar(sm)
cbar.set_label('Mean waiting time (min)', fontsize = 12)
cbar.ax.tick_params(labelsize=12)
plt.tight_layout()

map_regi.plot(ax = ax, column='Mean waiting time', cmap=cmap)

f.savefig('cat_time_100000.png')
plt.show()

#%%

#counts = data_df.value_counts()

#time_RP.regi_policial_rp.value_counts()[RP] # to acces the value in a Pandas Series
##############################################

#Typo problem from 2017, where there is only 1 blankspace between RP and Metropolitana
#RP_Metropolitana_nord = data_df[data_df['regi_policial_rp'] == 'RP Metropolitana Nord']
#RP_Metropolitana_nord_2 = data_df[data_df['regi_policial_rp'] == 'RP  Metropolitana Nord']

#Also, from 'gener 2021' the month name is written all in lowercase







