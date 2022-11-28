#Chaky

# This folder is a copy of another repository called: "learn_git_a_bit"
This is the repository where I share my homework and the progress I make in the final project of the subject "Anàlisi i Visualització de Dades Massives".

In this folder you can find the code, plots and files needed for the study of the ditribution of hate crimes per police region (and other categorizations) in Catalonia between 2020 and 2021.

Article:

  -"MiniArticle_Adrian_Chacon.pdf"

Code:

  -"Chaky_Police.ipynb": python code that contains the last version used in order to obtain the results.
  
  The following libraries with the corresponding versions have been used:
  
    numpy >  1.20

    matplotlib > 3.4

    pandas > 1.3.3

    geopandas >  0.12.1


Plots:
First there has been some imaging to gasp a better knowledge of the subject and try to visualize the more meaningful subjects to cover.

The plots that where finaly most valuable were the following:

  -"dailypatrolsRP.png": bar plot of the daily patrols per RP (blue) with a line (red) that represents the total mean of daily patrols
  
  -"map_area.png": map of Catalonia divided by RP that represents logarithm of the number of daily patrols per RP per area in km^2
  
  -"map_mean_daily_patrols.png": map of Catalonia divided by RP that represents the daily patrols per RP
  
  -"map_popu.png": map of Catalonia divided by RP that represents the daily patrols per 100.000 inhabitants per RP
  
  -"mapa.png": plot of all the results together


Files: 

  -Files necessaries to plot the maps. 
  
   The set of files contains the limits of the "municipis", "comarques","vagueries", "províncies", Catalonia and "caps de municipi, 
   comarca i província" with a multiscale base.
   
     -"divisions-administratives-v2r1-municipis-1000000-20220801.cpg"
     
     -"divisions-administratives-v2r1-municipis-1000000-20220801.dbf"
     
     -"divisions-administratives-v2r1-municipis-1000000-20220801.prj"
     
     -"divisions-administratives-v2r1-municipis-1000000-20220801.sbn"
     
     -"divisions-administratives-v2r1-municipis-1000000-20220801.sbx"
     
     -"divisions-administratives-v2r1-municipis-1000000-20220801.shp"
     
     -"divisions-administratives-v2r1-municipis-1000000-20220801.shx"
     
  
  -File necessary to compute the number of inhabitants per RP: "PoblacioRP.xlsx".
     
     
All data used has been extracted from:

  https://www.amb.cat/es/web/area-metropolitana/municipis-metropolitans 
  
  https://www.naciodigital.cat/manresa/noticia/98203/denuncies-primer-estat-alarma-catalunya-pendents-tc
  
  https://www.icgc.cat/Descarregues/Cartografia-vectorial/Divisions-administratives 
  
  https://www.idescat.cat/indicadors/?id=aec&n=15182 
  
  https://analisi.transparenciacatalunya.cat/Seguretat/V-ctimes-o-persones-autores-de-delictes-d-odi-i-di/gci6-2ubm
