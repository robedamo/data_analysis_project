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