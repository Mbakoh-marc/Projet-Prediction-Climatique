import streamlit as st
from multipage import MultiPage
from Page_1 import app as page1
from Page_2 import app as page2

app = MultiPage()

# Ajout des pages dans l'application
app.add_page("Analyse Climatique", page1)
app.add_page("Prédiction climatique", page2)


if __name__ == "__main__":
    app.run()