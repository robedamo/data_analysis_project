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

#We have data from 2011. However we will only use the one from 2015 in order 
#study a more current situation. Moreover, we will work with the data until 
#2021 because we will relate the number of daily patrols with the population 
#and there is only population data until 2021.

results_df=results_df.loc[(results_df['any']=='2021') | 
                          (results_df['any']=='2020') |
                          (results_df['any']=='2019') |
                          (results_df['any']=='2018') |
                          (results_df['any']=='2017') |
                          (results_df['any']=='2016') |
                          (results_df['any']=='2015') ]
                          

#All the strings ARE NOT in the same type of letter!
abps_serveis=results_df.servei_origen_dotaci.str.upper()
print(set(abps_serveis))

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
              
print(set(abps_serveis))


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
serveis_list_=[letter[20:] for letter in serveis_list]

#We write in two lines some Serveis Regionals in order to do a clear label
serveis_list_[2]="RP TERRES\nDE L'EBRE"
serveis_list_[4]="RP METROPOLITANA\nBARCELONA"
serveis_list_[5]="RP PIRINEU\nOCCINDENTAL"
serveis_list_[7]="RP CAMP DE\nTARRAGONA"
serveis_list_[8]="RP METROPOLITANA\nSUD"
serveis_list_[9]="RP METROPOLITANA\nNORD"

print(serveis_list_)



#We only ploy the Serveis Regionals
plt.figure()
plt.title('Mean daily patrols per RP (2015-2021)')
plt.bar(serveis_list_[1:],serveis_mean_patrols_list[1:], 0.8, label='RP daily patrols')
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
"""
Now we want to represent the mean number of daily patrols per inhabitant in 
order to know if it is homhogeneous
"""

#Firs we import the data of the inhabitants for comarques and then we will
#classify them for regions policials. 

poblacio_all_df =  pd.read_csv('poblacio_comarques.csv', sep=',', skiprows = 9)

#We will only choose 2015-2021 because some delimitations changed before that.
#Also, we only want the comarcas and in our data set there is inhabitants per
#Catalunya, per ambits and per provincia
poblacio_df=poblacio_all_df[poblacio_all_df.columns[:8]]

poblacio_df = poblacio_df.drop(labels=range(42, 55), axis=0)

#Now we make the mean of the population for each comarca
mean_comarca = poblacio_df.loc[:, ["2021","2020","2019", "2018", "2017", "2016", "2015"]].mean(axis = 1)

#We obtain the name of the comarques in the same order as the mean of
#inhabitants
nom_comarca= poblacio_df[poblacio_df.columns[0]]

#We transform our panda series to lists
mean_comarques=[]
comarques=[]

for comarca in nom_comarca:
    comarques.append(comarca)

for mean in mean_comarca:
    comarques.append(mean)

#%%

#We have to sum all the inhabitants per comarca in order to obtain the number
#of inhabitants per RP, which is what we want.

#First, we create the dictionary
RP_METROPOLITANA_NORD = ["Maresme", 'Vallès Occidental', 'Vallès Oriental']
RP_GIRONA = ['Alt Empordà', 'Gironès', 'Selva', 'Garrotxa', 'Ripollès',
             "Pla de l'Estany", "Baix Empordà"]
RP_CENTRAL = ['Osona', 'Berguedà', 'Solsonès', 'Bages', 'Anoia', 'Moianès']
RP_METROPOLITANA_SUD = ['Baix Llobregat', 'Garraf', 'Alt Penedès']
RP_CAMP_DE_TARRAGONA = ['Baix Penedès', 'Alt Camp', 'Tarragonès', 'Conca de Barberà', 'Baix Camp','Priorat']
RP_TERRES_DE_EBRE = ["Ribera d'Ebre", "Terra Alta","Baix Ebre", "Montsià"]
RP_PONENT = ['Segrià', 'Garrigiues', "Pla d'Urgell", "Urgell","Segarra", "Noguera", "Garrigues"]
RP_PIRINEU_OCCIDENTAL = ["Pallars Jussà","Alt Urgell", "Pallars Sobirà", "Alta Ribagorça", "Val d'Aran", "Cerdanya"]

comarques = RP_METROPOLITANA_NORD + RP_GIRONA + RP_CENTRAL + RP_METROPOLITANA_SUD\
    + RP_CAMP_DE_TARRAGONA + RP_TERRES_DE_EBRE + RP_PONENT + RP_PIRINEU_OCCIDENTAL
    
comarq_dict = {'RP METROPOLITANA NORD':RP_METROPOLITANA_NORD, 
               "RP GIRONA":RP_GIRONA, 'RP CENTRAL':RP_CENTRAL, "RP METROPOLITANA SUD":RP_METROPOLITANA_SUD,
               "RP CAMP DE TARRAGONA":RP_CAMP_DE_TARRAGONA, 
               "RP TERRES DE L'EBRE":RP_TERRES_DE_EBRE,"RP PONENT": RP_PONENT, 
               "RP PIRINEU OCCIDENTAL": RP_PIRINEU_OCCIDENTAL}


        


