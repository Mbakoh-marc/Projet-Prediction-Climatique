import streamlit as st
from sklearn.preprocessing import PolynomialFeatures
import joblib
import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    # Chargement les données depuis un fichier Excel
    df = pd.read_excel("data_clean_idf.xlsx")
    # Création d'une nouvelle colonne pour l'année de la décennie
    df['Decade'] = (df['YEAR'] // 10) * 10
    return df

def predict_temperature_decenie(year, month, model):
    # Déterminer la décennie correspondant à l'année entrée
    decade = (year // 10) * 10
    # Générer les années de cette décennie
    decade_years = range(decade, decade + 10)
    # Prédire les températures pour chaque année de cette décennie
    predictions = []
    for year in decade_years:
        # Prépareration les données pour la prédiction
        data = pd.DataFrame({"year": [year], "month": [month]})
        # Recréation et ajustement des fonctionnalités polynomiales
        poly_features = PolynomialFeatures(degree=4)
        new_data_poly = poly_features.fit_transform(data)
        # prédiction
        prediction = model.predict(new_data_poly)[0]
        predictions.append(prediction)
    # Calculer la moyenne des températures prédites
    average_prediction = sum(predictions) / len(predictions)
    return average_prediction
def predict_temperature (year, month, model):
    # Prépareration les données pour la prédiction
    data = pd.DataFrame({"year": [year], "month": [month]})
    # Recréation et ajustement des fonctionnalités polynomiales
    poly_features = PolynomialFeatures(degree=4)
    new_data_poly = poly_features.fit_transform(data)
    # prédiction
    prediction = model.predict(new_data_poly)[0]
    return prediction


def plot_temp_evolution(selected_month, decade_data, average_prediction):

    st.write(""" Ce graphique présente l'évolution des températures moyennes pour le mois sélectionné au cours de chaque décennie. 
    De plus, il affiche la valeur moyenne de la température pour la décennie correspondant à l'année entrée.""")
    # Création de la figure et de l'axe
    fig, ax = plt.subplots()
    # Tracé des températures moyennes par décennie
    ax.plot(decade_data['Decade'], decade_data['TM'], label='Température moyenne', color='blue')
    # Ajout de la prédiction sur le graphique
    ax.axhline(y=average_prediction, color='red', linestyle='--', label='Prédiction')
    # Ajout de titres et d'étiquettes d'axe
    ax.set_title(f'Évolution de la température pour le mois de {selected_month} par décennie')
    ax.set_xlabel('Décennie')
    ax.set_ylabel('Température moyenne (°C)')
    ax.legend()
    # Affichage du graphique
    st.pyplot(fig)


def app():
    st.title("Prédiction de la Température en Île-de-France")

    # Chargement du modèle de machine learning
    model = joblib.load("model_polynomial_degree5.pkl")

    st.write("""Ce modèle est en mesure de prédire la température moyenne mensuelle en Île-de-France en
     fonction de l'année, avec une marge d'incertitude relative de ±1,2°C.""")

    # Formulaire pour entrer les données de prédiction
    year = st.number_input("Entrez l'année", min_value=1950, max_value=2080, step=1)
    month = st.number_input("Entrez le mois", min_value=1, max_value=12, step=1)

    if st.button("Prédire"):
        # Prédiction de la température
        prediction = predict_temperature(year, month, model)
        st.write(f"La température moyenne prédite pour {year}-{month} est de {prediction:.2f}°C")
        prediction = predict_temperature_decenie(year, month, model)
        st.write(f"La température moyenne prédite pour le mois {month} de la décénie {(year // 10) * 10} est de {prediction:.2f}°C")

        # Chargement des données
        df = load_data()
        # Filtrage des données en fonction du mois sélectionné
        selected_month_data = df[df['MONTH'] == month]
        # Regroupement par décennie et calcul de la température moyenne
        decade_data = selected_month_data.groupby('Decade').mean().reset_index()
        # Affichage du graphique
        plot_temp_evolution(month, decade_data, prediction)


if __name__ == "__main__":
    app()