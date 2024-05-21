import pandas as pd 
import matplotlib as plt 
import seaborn as sns 
import os 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np



chemin_data = r'/Users/MSI/Desktop/Projet_pro'
dataset =  'data_clean.xlsx'
filepath = os.path.join(chemin_data, dataset)



df = pd.read_excel(filepath)
df = df.drop(columns=['GLOT'])


valeurs_Null = df.isnull().sum(axis=1)
lignes_avec_valeurs_manquantes = df[valeurs_Null> 0]

nombre_de_lignes_avec_valeurs_manquantes = len(lignes_avec_valeurs_manquantes)

print(f"Nombre de lignes avec des valeurs manquantes : {nombre_de_lignes_avec_valeurs_manquantes}")
print("Lignes avec des valeurs manquantes :")
print(lignes_avec_valeurs_manquantes)

#supression des espaces 
df.columns = df.columns.str.strip()


colonnes_supp = ['TXMIN', 'TNMAX',  'TMM', 'TMMIN', 'TMMAX', 'TSVM', 'TAMPLIM', 'INST']
df = df.drop(columns=colonnes_supp)



df = df[~((df['AAAAMM'].dt.year == 2024) & (df['AAAAMM'].dt.month == 4))]



df['AAAAMM'] = pd.to_datetime(df['AAAAMM'])

df['Année'] = df['AAAAMM'].dt.year
df['Décennie'] = (df['Année'] // 10) * 10

print(df.tail())
#def des saisons
df['AAAAMM'] = pd.to_datetime(df['AAAAMM'])
df['Saison'] = df['AAAAMM'].dt.month.apply(lambda x: 'Hiver' if x in [12, 1, 2] else 'Printemps' if x in [3, 4, 5] else 'Été' if x in [6, 7, 8] else 'Automne')
##########################################################################################################
########################################################""""""""""""""
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Assuming 'df' is already defined and contains the relevant data
mean_temp_season_decade = df.groupby(['Saison', 'Décennie'])['TM'].mean().reset_index()
mean_temp_season_decade['Diff'] = mean_temp_season_decade.groupby('Saison')['TM'].diff().fillna(0)

def determine_color(diff):
    if diff > 0:
        return 'red'
    else:
        return 'green'

mean_temp_season_decade['Color'] = mean_temp_season_decade['Diff'].apply(determine_color)

plt.figure(figsize=(12, 7))
seasons = mean_temp_season_decade['Saison'].unique()

for season in seasons:
    season_data = mean_temp_season_decade[mean_temp_season_decade['Saison'] == season]
    plt.plot(season_data['Décennie'], season_data['TM'], marker='o', color='black', label=f"{season}")
    for i in range(1, len(season_data)):
        plt.plot(season_data['Décennie'].iloc[i-1:i+1], season_data['TM'].iloc[i-1:i+1],
                 marker='o', color=season_data['Color'].iloc[i])
    
    # Ajouter des annotations pour indiquer la saison au premier point
    first_point = season_data.iloc[0]
    plt.annotate(season, (first_point['Décennie'], first_point['TM']), textcoords="offset points", xytext=(0,5), ha='center')

red_line = mlines.Line2D([], [], color='red', marker='o', linestyle='-', markersize=5, label='Augmentation')
green_line = mlines.Line2D([], [], color='green', marker='o', linestyle='-', markersize=5, label='Diminution')

handles, labels = plt.gca().get_legend_handles_labels()
handles.extend([red_line, green_line])
labels.extend(['Augmentation', 'Diminution'])

plt.legend(handles=handles, labels=labels, title='Saison', bbox_to_anchor=(1, 1), loc='upper left', fontsize=6)

plt.title('Température Moyenne par Décennie et par Saison (1950-2024)', fontsize=12)
plt.xlabel('Décennie', fontsize=10)
plt.ylabel('Température Moyenne (°C)', fontsize=10)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.show()


#######################################################
##########################################################""""""""""""""
mean_temp_max_min_decade = df.groupby('Décennie').agg({'TX': 'mean', 'TN': 'mean'}).reset_index()

plt.figure(figsize=(14, 8))

sns.lineplot(data=mean_temp_max_min_decade, x='Décennie', y='TX', marker='o', color='limegreen', label='Température Maximale')

sns.lineplot(data=mean_temp_max_min_decade, x='Décennie', y='TN', marker='o', color='lightgreen', label='Température Minimale')

plt.title('Température Maximale et Minimale Moyenne par Décennie (1950-2024)')
plt.xlabel('Décennie')
plt.ylabel('Température (°C)')
plt.legend(title='Type de Température')


plt.ylim(0, 20)
plt.yticks(np.arange(0, 21, 2), fontsize=10)
plt.grid(True, linestyle='--', linewidth=0.5)

plt.show()








########################################################################################################################################""
mean_temp_max_min_season_decade = df.groupby(['Saison', 'Décennie']).agg({'TX': 'mean', 'TN': 'mean'}).reset_index()

plt.figure(figsize=(20, 8))
sns.lineplot(data=mean_temp_max_min_season_decade, x='Décennie', y='TX', hue='Saison', marker='o', palette='viridis', legend='full')
plt.title('Température Maximale Moyenne par Décennie et par Saison (1950-2024)')
plt.xlabel('Décennie')
plt.ylabel('Température Maximale Moyenne (°C)')
plt.legend(title='Saison', bbox_to_anchor=(1, 1), loc='upper left')
plt.grid(True)

for i in range(mean_temp_max_min_season_decade.shape[0]):
    plt.text(x=mean_temp_max_min_season_decade['Décennie'][i], 
             y=mean_temp_max_min_season_decade['TX'][i], 
             s=f"{mean_temp_max_min_season_decade['TX'][i]:.1f}", 
             color='black', 
             ha='center', 
             va='bottom')



plt.show()

plt.figure(figsize=(14, 8))
sns.lineplot(data=mean_temp_max_min_season_decade, x='Décennie', y='TN', hue='Saison', marker='o', palette='viridis', legend='full')
plt.title('Température Minimale Moyenne par Décennie et par Saison (1950-2024)')
plt.xlabel('Décennie')
plt.ylabel('Température Minimale Moyenne (°C)')
plt.legend(title='Saison', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

for i in range(mean_temp_max_min_season_decade.shape[0]):
    plt.text(x=mean_temp_max_min_season_decade['Décennie'][i], 
             y=mean_temp_max_min_season_decade['TN'][i], 
             s=f"{mean_temp_max_min_season_decade['TN'][i]:.1f}", 
             color='black', 
             ha='center', 
             va='bottom')
    

plt.show()

#########################################################################################################################################
#####################################""""""""

plt.figure(figsize=(14, 8))
sns.swarmplot(data=df, x='Décennie', y='RR', hue='Saison', palette='cubehelix')
plt.title('Distribution des Précipitations par Saison et par Décennie (1950-2024)')
plt.xlabel('Décennie')
plt.ylabel('Précipitations (mm)')
plt.legend(title='Saison', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()
#######################################################################################################################################
# 4. Corrélation entre les variables météorologiques
corr_matrix = df[['RR', 'PMERM', 'TX', 'TN', 'TM', 'UMM', 'ETP', 'FFM']].corr()

plt.figure(figsize=(14, 7))
sns.heatmap(corr_matrix, annot=True, cmap='viridis', center=0)
plt.title('Matrice de Corrélation entre les Variables Météorologiques')
plt.show()

####################################################################################################################################""
mean_humidity_monthly_decade = df.groupby(['Décennie', df['AAAAMM'].dt.month])['UMM'].mean().reset_index()
mean_humidity_monthly_decade = mean_humidity_monthly_decade.rename(columns={'AAAAMM': 'Month'})

decade_colors = sns.color_palette('viridis', n_colors=len(mean_humidity_monthly_decade['Décennie'].unique()))

plt.figure(figsize=(12, 6))
sns.barplot(data=mean_humidity_monthly_decade, x='Month', y='UMM', hue='Décennie', palette=decade_colors, edgecolor='black')
plt.title('Variation de l\'humidité moyenne par mois et par décennie')
plt.xlabel('Mois')
plt.ylabel('Humidité moyenne')
plt.xticks(rotation=45)
plt.legend(title='Décennie', bbox_to_anchor=(1, 1), loc='upper left')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()
###########################################################################################################################################


mean_wind_speed_season_year = df.groupby(['Saison', 'Année'])['FFM'].mean().reset_index()
mean_wind_speed_season_decade = df.groupby(['Saison', 'Décennie'])['FFM'].mean().reset_index()

plt.figure(figsize=(14, 8))
sns.barplot(data=mean_wind_speed_season_decade, x='Décennie', y='FFM', hue='Saison', palette='viridis', edgecolor='black')
plt.title('Variation de la force moyenne du vent par saison et par décennie')
plt.xlabel('Décennie')
plt.ylabel('Force moyenne du vent (FFM)')
plt.legend(title='Saison', bbox_to_anchor=(1, 1), loc='upper left')
plt.grid(True)
plt.show()

########################################################################################################################################
mean_pressure_season_decade = df.groupby(['Saison', 'Décennie'])['PMERM'].mean().reset_index()

plt.figure(figsize=(14, 8))
sns.barplot(data=mean_pressure_season_decade, x='Décennie', y='PMERM', hue='Saison', palette='viridis', edgecolor='black')
plt.title('Variation de la moyenne mensuelle des pressions mer moyennes par saison et par décennie')
plt.xlabel('Décennie')
plt.ylabel('Moyenne des pressions mer moyennes (PMERM) (hPa)')
plt.legend(title='Saison', bbox_to_anchor=(1, 1), loc='upper left')
plt.grid(True)
plt.show()