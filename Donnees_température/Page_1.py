import streamlit as st
from Analyses_Graphiques import (load_data, calculate_decade_means, plot_temperature_by_decade,
                                 plot_monthly_comparison, plot_seasonal_temperature_by_decade,
                                 plot_seasonal_comparison, plot_seasonal_difference, plot_monthly_difference,
                                 plot_humidity_moyenne_decennie, plot_extreme_temperatures, plot_temp_max_min_decennie)

def app():

    st.title("Evolution de la température en Île-de-France")

    # Chargement des données
    df = load_data("data_clean_idf.xlsx")

    # Affichage des données
    st.write("""Ce dataset contient les données historiques des températures de l'Île-de-France,
     couvrant la période de 1950 à 2024. 
     Les données représentent les moyennes mensuelles des températures et ont été obtenues à partir du site officiel de Météo-France, 
     notamment via la plateforme meteo.data.gouv.""")
    st.dataframe(df.head())

    # Calculer les moyennes des températures par décennie
    df_decade = calculate_decade_means(df)

    # _____________________________________________________________________________________

    st.subheader("Visualisation de l'Évolution Climatique à Travers des Graphiques\n")
    st.write("""✅ Dans cette section, nous analyserons les différents paramètres de température afin de clarifier l'évolution des températures 
    mensuelles moyennes. Nous effectuerons des analyses de saisonnalité ainsi que des analyses par décennies.\n\n""")

    # Affichage du graphique de l'évolution de l'humidité moyenne par décennie :
    st.write("⛅ EVOLUTION DE L'HUMIDITE MOYENNE PAR DECENIE")
    plot_humidity_moyenne_decennie(df)
    st.write("""✅ Ce graphique montre clairement une tendance à la baisse de l'humidité moyenne mensuelle observée en Île-de-France pour chaque décennie allant de 1950 à 2000.
     Dans la décennie de 1950, l'humidité moyenne était proche de 80,5 %, tandis que dans la décennie de 2020, elle tend vers 76 %.
     Cela montre une diminution conséquente de 4,5 % d'humidité, ce qui pourrait indiquer une augmentation des températures, entraînant une baisse de l'humidité.\n""")

    # _____________________________________________________________________________________

    # Afficher le graphique de la comparaison des températures moyennes pour chaque saison
    st.write("⛅ LES TROIS JOURNEES LES PLUS CHAUDES ET PLUS FROIDES")
    plot_extreme_temperatures(df)
    st.write("""✅ Ce graphique illustre que les mois de juin et d'août affichent les températures les plus élevées,
     tandis que février enregistre les températures les plus basses. De plus, on observe une tendance à l'augmentation 
     des températures les plus basses au fil du temps. Le graphique suivant fournira une réponse à la question de savoir si ce phénomène indique un réchauffement climatique.\n""")


    # _____________________________________________________________________________________

    # Affichage du graphique de l'évolution des températures moyennes maximales et minimales en fonction du temps
    st.write("⛅ EVOLUTION DES TEMPERATURES MOYENNES MAXIMALES ET MINIMALES PAR DECENIE")
    plot_temp_max_min_decennie(df)
    st.write("""✅ Ces observations confirment notre hypothèse précédente : les températures moyennes maximales et minimales augmentent régulièrement par décennie.
     Cette tendance est particulièrement notable entre les décennies de 1950 et 2020, où l'augmentation des températures moyennes maximales et minimales indique 
     clairement un réchauffement climatique.\n""")

    # _____________________________________________________________________________________

    # Affichage du graphique de  comparaison des températures moyennes mensuelles entre deux périodes
    st.write("⛅ COMPARAISON DES TEMPERATURES MOYENNES MENSUELLES ENTRE 1950-1960 & 2010-2020")
    plot_monthly_comparison(df)
    st.write("""✅ Pour renforcer notre affirmation précédente, ce graphique démontre clairement que la température
     moyenne entre 1950 et 1960 est inférieure à celle entre 2010 et 2020. Cette comparaison précise souligne davantage
      le phénomène du réchauffement climatique au fil des décennies.\n""")

    # _____________________________________________________________________________________

    # Affichage du graphique de l'évolution de la température moyenne par décennie
    st.write("⛅ EVOLUTION DE LA TEMPERATURE MENSUELLE PAR DECENIE:")
    plot_temperature_by_decade(df_decade)
    st.write("""✅ En conclusion de cette problématique, ce graphique illustre clairement une tendance à la hausse de la température moyenne mensuelle au fil des décennies.
     Cette observation nous permet d'affirmer avec certitude que: NOTRE CLIMAT CONNAIT UN RECHAUFFEMENT CLIMATIQUE !!!\n\n""")

    # _____________________________________________________________________________________

    st.write("""🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤🌤\n
    \n Dans la section précédente, nous avons observé un réchauffement de notre climat. 
    À présent, nous examinerons les saisons pour détermier celles qui sont les plus impactées par ce phénomène.""")

    # Affichage du graphique de la différence de température moyenne par mois entre deux périodes
    st.write("⛅ DIFFERENCE DE TEMPERATURE MOYENNE PAR MOIS ENTRE 1950-1960 et 2010-2010 :")
    plot_monthly_difference(df)
    st.write("""✅ Ce graphique compare les moyennes mensuelles décennales des climats entre 1950-1960 et 2010-2020,
     offrant ainsi une vue d'ensemble de l'évolution climatique. Il met en évidence que certains mois de l'année,
      tels que Mars, Mai et septembre, réagissent de manière moins significative à ce phénomène que d'autres. 
      Cela soulève la question de savoir si certaines saisons sont plus sensibles aux changements climatiques que d'autres.\n""")

    # _____________________________________________________________________________________

    # Affichage du graphique de l'évolution des températures moyennes par saison et par décennie
    st.write("""\n Pour repondre à la problématique posée nous avons trouvé judicieux de faire un graphe qui montre
    l'évolution des températures moyennes par saison et par décennie\n
    ⛅EVOLUTION DES TEMPERATURES MOYENNES PAR SAISON ET PAR DECENIE""")
    plot_seasonal_temperature_by_decade(df)
    st.write("""\n✅ Ce graphique révèle des tendances plus marquées pour les saisons d'été ,d'hiver, d'automne et moins prononcées pour la saison du printemps. 
    Cela renforcerait-il notre hypothèse selon laquelle certaines saisons sont plus touchées que d'autres par ce phénomène ? ?""")

    # _____________________________________________________________________________________

    # Affichage du graphique de la comparaison des températures moyennes pour chaque saison
    st.write("⛅ COMPARAISON DES TEMPERATURES MOYENNES SAISONEIERES ENTRE 1950-1960 & 2010-2020")
    plot_seasonal_comparison(df)
    st.write("""\n✅ Ces graphiques révèlent une différence significative entre les saisons d'hiver, d'été et d'automne de 1950-1960 et 2010-2020, tandis que la différence est plutôt minimale pour le printemps. 
    Cette observation soulève l'intérêt d'examiner de plus près ces différences et de déterminer leur valeur moyenne.\n""")

    # _____________________________________________________________________________________

    # Affichage du graphique de la différence de température moyenne par saison entre deux périodes
    st.write("⛅ DIFFERENCE DE TEMPERATURE MOYENNE PAR SAISON ENTRE 1950-1960 & 2010-2020 ")
    plot_seasonal_difference(df)
    st.write("""\n✅ Nous observons une augmentation moyenne de 1,51°C pour l'hiver, 1,74°C pour l'été, 1,52°C pour l'automne et 0,85°C 
    pour le printemps au cours de ces 6 dernières décénies. Cette analyse nous permet de conclure que le phénomène de réchauffement 
    climatique a un impact plus marqué sur certaines saisons, telles que l'hiver et l'été et l'automne que sur d'autres, comme le printemps.\n""")

    # _____________________________________________________________________________________
    st.subheader("\nConclusion\n")

    st.write("""\n🏙️ Les données analysées révèlent une tendance claire au réchauffement climatique au cours des dernières décennies.
     Les températures moyennes ont augmenté de manière significative pour toutes les saisons, avec des augmentations plus prononcées 
     observées pendant les saisons d'hiver ,d'été et d'automne. Cette augmentation progressive des températures met en évidence l'impact du changement 
     climatique sur les différentes saisons. Ces observations soulignent l'importance de prendre des mesures pour atténuer les effets du réchauffement
      climatique et s'adapter aux changements environnementaux.\n""")


