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
#We remove the data of 2022 (since there is only 3 values of different RP and ABP (not correlated))
data_df = data_df.set_index('any')
data_df = data_df.drop('2022')
data_df = data_df.reset_index()


#Also erase the 'Divisió de Transport' RP since it has not analysis value
data_df = data_df.set_index('regi_policial_rp')
data_df = data_df.drop('Divisió de Transport')
data_df = data_df.reset_index()


#Since there is 2 RP Metropolitana Nord we need to change the name of these strings
data_df = data_df.replace('RP  Metropolitana Nord', 'RP Metropolitana Nord')
#replace finds all 'RP  Metropolitana Nord' in the dataframe and substitutes with
#'RP Metropolitana Nord' (only one blankspace between 'RP and Metropolitana')

print(data_df['regi_policial_rp'].value_counts())
#There are more values for RP Metropolitana Nord since there are more ABPs in it


#We need to change the number of visits to a integer, since now is considered an string
data_df['nombre_de_visites'] = data_df['nombre_de_visites'].astype('int')

#We also need to transform the data of time into seconds to work easier




#%%
#Specific ABP
ABP = 'Alt Urgell'
single_ABP = data_df[data_df['rea_b_sica_policial_abp'] == 'ABP ' + ABP]

mes_visites = pd.DataFrame({'Mes':single_ABP.loc[:,'nom_mes'], 'Nombre visites':single_ABP.loc[:,'nombre_de_visites']})
mes_visites = mes_visites.set_index('Mes')

#To plot the number of visits in one specific ABP
mes_visites.plot(kind='bar', title='ABP '+ABP, xlabel='Month', ylabel='Number of visits', 
                 rot=60, stacked=False, legend=False)



#%%
#We want to plot the number of visits in every RP from 2011 to 2021

#We create a DataFrame with 2 columns with the RP and number of visits
visites_RP = data_df[['regi_policial_rp','nombre_de_visites']].copy()

number_of_years = 10 #to divide and obtain the mean for all years (from 2011 to 2021)

#Write all the RPs in a list
list_RP = [i for i in (visites_RP['regi_policial_rp'].value_counts()).index]

mean_visites_RP = []
visites_RP = visites_RP.set_index('regi_policial_rp')

for RP in list_RP:
    specific_RP = visites_RP.loc[RP]
    #Compute the mean for all RPs, round the number and append into the list
    mean_visites_RP.append(np.round(sum(specific_RP.nombre_de_visites)/number_of_years, decimals=0))

mean_visites_RP = [int(i) for i in mean_visites_RP] #transform the mean visits into integers

#Create a new DataFrame in order to plot
mean_visites_RP = pd.DataFrame(data=mean_visites_RP, index=list_RP, columns=['Mean number of visits'])


#Plot the average number of visits per year for every RP
mean_visites_RP.plot(kind='bar', ylabel='Average number fo visits per year', 
                     rot=90, legend=False)
plt.tight_layout()


#%%
#We want to plot the average time that takes to be attended after entering the police department

times_df = data_df[['mitjana_temps_espera']].copy()

times_df['mitjana_temps_espera'] = pd.to_datetime(times_df['mitjana_temps_espera'])

#%%

print(times_df.mitjana_temps_espera.dt.minute) #to obtain the minutes




#print(df.Date_time.dt.hour.head())

#%%

#time_format = '%H:%M:%S'

data_df['mitjana_temps_espera'] = data_df['mitjana_temps_espera'].datatime.hour * 3600 + \
                                  data_df['mitjana_temps_espera'].datatime.minute * 60 + \
                                  data_df['mitjana_temps_espera'].datatime.second





#%%
#Plot with circles of different sizes?
#Maybe the size of the circle is the mean time that every ABP takes (in a year).
#Flowing data (web or library)


#%%

#counts = data_df.value_counts()
#ABP_Granollers_mes_visites = ABP_Granollers[['mes','nombre_de_visites']]
##############################################

#Typo problem from 2017, where there is only 1 blankspace between RP and Metropolitana
#RP_Metropolitana_nord = data_df[data_df['regi_policial_rp'] == 'RP Metropolitana Nord']
#RP_Metropolitana_nord_2 = data_df[data_df['regi_policial_rp'] == 'RP  Metropolitana Nord']

#Also, from 'gener 2021' the month name is written all in lowercase







