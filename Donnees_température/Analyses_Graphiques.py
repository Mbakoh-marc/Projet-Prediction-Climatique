import pandas as pd
import matplotlib.pyplot as plt
import calendar
import streamlit as st

# Chargement des données
def load_data(file_path):
    return pd.read_excel(file_path)

# Calcul des moyennes des températures moyennes par décennie
def calculate_decade_means(df):
    df['Decade'] = df['YEAR'] // 10 * 10
    return df.groupby('Decade').mean()

def plot_humidity_moyenne_decennie(df):
    df['Decade'] = df['YEAR'] // 10 * 10  # Calcul de la décennie
    df_decade = df.groupby('Decade').mean()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(df_decade.index, df_decade['UMM'], label='Humidité moyenne', color='blue')
    ax.set_title('Évolution de l\'humidité moyenne par décennie')
    ax.set_xlabel('Décennie')
    ax.set_ylabel('Humidité moyenne (%)')
    ax.grid(True, linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

def plot_extreme_temperatures(df):
    sorted_df_max = df.sort_values(by='TX', ascending=False)
    sorted_df_min = df.sort_values(by=' TN', ascending=True)

    top_highest_temps = sorted_df_max.head(3)
    top_lowest_temps = sorted_df_min.head(3)

    xticks_labels_max = [f"{row['YEAR']}-{row['MONTH']}" for _, row in top_highest_temps.iterrows()]
    xticks_labels_min = [f"{row['YEAR']}-{row['MONTH']}" for _, row in top_lowest_temps.iterrows()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 3.7))
    ax1.bar(xticks_labels_max, top_highest_temps['TX'], color='red')
    ax1.set_title("Journées les plus chaudes")
    ax1.set_ylabel("Température (°C)")

    ax2.bar(xticks_labels_min, top_lowest_temps[' TN'], color='blue')
    ax2.set_title("Journées les plus froides")

    plt.tight_layout()
    st.pyplot(fig)

def plot_temp_max_min_decennie(df):
    df['Decade'] = df['YEAR'] // 10 * 10  # Calcul de la décennie
    df_decade = df.groupby('Decade').mean()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(df_decade.index, df_decade['TX'], label='Température maximale moyenne', color='red')
    ax.plot(df_decade.index, df_decade[' TN'], label='Température minimale moyenne', color='blue')
    ax.set_title('Évolution des températures moyennes par décennie')
    ax.set_xlabel('Décennie')
    ax.set_ylabel('Température moyenne (°C)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Tracé de l'évolution des températures moyennes par décennie
def plot_temperature_by_decade(df_decade):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(df_decade.index, df_decade['TM'], label='Température moyenne', color='blue')
    ax.set_title('Évolution de la température moyenne par décennie')
    ax.set_xlabel('Décennie')
    ax.set_ylabel('Température moyenne (°C)')
    ax.grid(True, linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

# Tracé de la comparaison des températures moyennes mensuelles entre deux périodes
def plot_monthly_comparison(df):
    period1 = df[(df['YEAR'] >= 1950) & (df['YEAR'] <= 1960)]
    period2 = df[(df['YEAR'] >= 2010) & (df['YEAR'] <= 2020)]

    monthly_temp1 = period1.groupby(period1['MONTH'])['TM'].mean()
    monthly_temp2 = period2.groupby(period2['MONTH'])['TM'].mean()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(monthly_temp1.index, monthly_temp1.values, label='1950-1960', color='blue')
    ax.plot(monthly_temp2.index, monthly_temp2.values, label='2010-2020', color='red')
    ax.set_title('Comparaison des températures moyennes mensuelles entre 1950-1960 et 2010-2020')
    ax.set_xlabel('Mois')
    ax.set_ylabel('Température moyenne (°C)')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'])
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

# Fonction pour déterminer la saison
def get_season(month):
    if month in [12, 1, 2]:
        return 'Hiver'
    elif month in [3, 4, 5]:
        return 'Printemps'
    elif month in [6, 7, 8]:
        return 'Été'
    else:
        return 'Automne'

# Tracé de l'évolution des températures moyennes par saison et par décennie
def plot_seasonal_temperature_by_decade(df):
    df['Saison'] = df['MONTH'].apply(get_season)
    seasonal_temp = df.groupby(['Decade', 'Saison'])['TM'].mean().reset_index()
    seasonal_temp_pivot = seasonal_temp.pivot(index='Decade', columns='Saison', values='TM')

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for season in seasonal_temp_pivot.columns:
        ax.plot(seasonal_temp_pivot.index, seasonal_temp_pivot[season], label=season)

    ax.set_title('Évolution des températures moyennes par saison et par décennie')
    ax.set_xlabel('Décennie')
    ax.set_ylabel('Température moyenne (°C)')
    ax.legend(title='Saison')
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Comparaison des températures moyennes pour chaque saison
def plot_seasonal_comparison(df):
    period1 = df[(df['YEAR'] >= 1950) & (df['YEAR'] <= 1960)].copy()
    period2 = df[(df['YEAR'] >= 2010) & (df['YEAR'] <= 2020)].copy()
    period1['Saison'] = period1['MONTH'].apply(get_season)
    period2['Saison'] = period2['MONTH'].apply(get_season)

    seasonal_temp1 = period1.groupby(['Saison', 'MONTH'])['TM'].mean().unstack(level=0)
    seasonal_temp2 = period2.groupby(['Saison', 'MONTH'])['TM'].mean().unstack(level=0)

    def reorder_months(df):
        return df.reindex([12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    seasonal_temp1 = reorder_months(seasonal_temp1)
    seasonal_temp2 = reorder_months(seasonal_temp2)

    seasons = ['Hiver', 'Printemps', 'Été', 'Automne']
    months = ['Déc', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov']

    fig, axes = plt.subplots(2, 2, figsize=(10, 6))

    for i, season in enumerate(seasons):
        ax = axes[i // 2, i % 2]
        ax.plot(range(1, 13), seasonal_temp1[season], label='1950-1960', color='blue')
        ax.plot(range(1, 13), seasonal_temp2[season], label='2010-2020', color='red')
        ax.set_title(f'Comparaison des températures moyennes pour {season}')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Température moyenne (°C)')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(months)
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    st.pyplot(fig)

# Tracé de la différence de température moyenne par saison entre deux périodes
def plot_seasonal_difference(df):
    period1 = df[(df['YEAR'] >= 1950) & (df['YEAR'] <= 1960)].copy()
    period2 = df[(df['YEAR'] >= 2010) & (df['YEAR'] <= 2020)].copy()
    period1['Saison'] = period1['MONTH'].apply(get_season)
    period2['Saison'] = period2['MONTH'].apply(get_season)

    seasonal_temp_evolution_period1 = period1.groupby(['YEAR', 'Saison'])['TM'].mean().unstack()
    seasonal_temp_evolution_period2 = period2.groupby(['YEAR', 'Saison'])['TM'].mean().unstack()

    mean_seasonal_temp_evolution_period1 = seasonal_temp_evolution_period1.mean()
    mean_seasonal_temp_evolution_period2 = seasonal_temp_evolution_period2.mean()

    diff_seasonal_temp_evolution = mean_seasonal_temp_evolution_period2 - mean_seasonal_temp_evolution_period1

    fig, ax = plt.subplots(figsize=(5, 4))
    diff_seasonal_temp_evolution.plot(kind='bar', color='blue', ax=ax)
    ax.set_title("Evolution de la température entre les saisons sur les décennies 1950-1960 et 2010-2020")
    ax.set_xlabel('Saison')
    ax.set_ylabel("Température moyenne (°C)")
    plt.tight_layout()
    st.pyplot(fig)

# Tracé de la différence de température moyenne par mois entre deux périodes
def plot_monthly_difference(df):
    period1 = df[(df['YEAR'] >= 1950) & (df['YEAR'] <= 1960)].copy()
    period2 = df[(df['YEAR'] >= 2010) & (df['YEAR'] <= 2020)].copy()
    period1['Mois'] = period1['MONTH']
    period2['Mois'] = period2['MONTH']

    month_labels = [calendar.month_name[i] for i in range(1, 13)]

    monthly_temp_evolution_period1 = period1.groupby(['YEAR', 'Mois'])['TM'].mean().unstack()
    monthly_temp_evolution_period2 = period2.groupby(['YEAR', 'Mois'])['TM'].mean().unstack()

    mean_monthly_temp_evolution_period1 = monthly_temp_evolution_period1.mean()
    mean_monthly_temp_evolution_period2 = monthly_temp_evolution_period2.mean()

    diff_monthly_temp_evolution = mean_monthly_temp_evolution_period2 - mean_monthly_temp_evolution_period1

    fig, ax = plt.subplots(figsize=(7, 4.5))
    diff_monthly_temp_evolution.plot(kind='bar', color='blue', ax=ax)
    ax.set_title("Différence de température moyenne entre chaque mois sur les décennies 1950-1960 et 1990-2000")
    ax.set_xlabel('Mois')
    ax.set_xticks(range(12))
    ax.set_xticklabels(month_labels)
    ax.set_ylabel("Différence de température moyenne (°C)")
    plt.tight_layout()
    st.pyplot(fig)

