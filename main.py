import random
from helpers import rapport_creator, markdown_to_html, features_from_form
import streamlit as st
from base64 import b64encode
import pickle as pkl
import numpy as np



options = {
    'Sexe': ["homme", "femme"],
    'Douleur Spontanée': [
        'continue',
        'intense',
        'irradiée', 
        'non',
        'occassionnellement', 
        'oui', 
        "oui irradiante vers l'oreil", 
        'prolongée', 
        'pulsatile', 
        'récente'
    ],
    'Douleur Provoquée': [
        'au contact',
        'chaud',
        'effort physique',
        'froid',
        'mastication',
        'non',
        'parfois a la mastication',
        'position allongée',
        'pression', 
        'sucre'
    ],
    'Mobilité': ["oui", "non", "1" , '1+'],
    'Vitalité': [
        'dent morte',
        'dent vivante'
    ],
    'Palpation Apicale': [
        'douleur avec comblement',
        'douleur si pression',
        'negatif',
        'oui'
    ],
    'Fievre': ['non', 'oui', 'oui , locale'],
    'Asthenie': ['non', 'oui'],
    'Odeur Fétide': [
        'non',
        'oui', 
        'oui avec mauvais gout'
    ],
    'Médication ATG': [
        'efficace',
        'efficace , si stade avancee non', 
        'non efficace',
    ],
    'Soulager': [
        'brossage',
        'eviter la cause',
        'eviter la mastication',
        'froid',
        'parfois par le froid',
        'rien' ,
        'sans contact'
    ],
    'Observations Exobuccales ( remarque generale ) ': 
    [
        'asymétrie faciale',
        'dent en main',
        "limitation de l'ouverture buccale + capuchon muqueux postérieur mandibulaire",
        'non',
        'parfois orifice',
        'saignement au brossage',
        'sensation de dent longue',
        'trauma qui affecte la région'
    ]
}
description = {
    'Douleur Spontanée': 'Douleur qui survient sans aucune stimulation ou contact avec les dents affectées.',
    'Douleur Provoquée': 'Douleur qui survient lorsqu\'une stimulation ou un contact est appliqué sur les dents affectées.',
    'Mobilité': 'Un ou plusieurs dents peuvent se déplacer de leur position normale lorsqu\'elles sont poussées avec une pression légère à modérée.',
    'Vitalité': 'Capacité des dents à répondre à un stimulus thermique ou électrique, indiquant la santé ou la maladie de la pulpe dentaire.',
    'Palpation Apicale': 'Sensation de douleur à la pression sur la région de l\'apex de la dent affectée.',
    'Fievre': 'Température corporelle élevée, indiquant souvent une infection ou une inflammation.',
    'Asthenie': 'Faiblesse générale et fatigue, pouvant indiquer une infection systémique ou une maladie.',
    'Odeur Fétide': 'Odeur désagréable et nauséabonde provenant de la bouche ou de la dent affectée.',
    'Médication ATG': 'Antibiotiques, analgésiques et anti-inflammatoires prescrits pour soulager la douleur et lutter contre l\'infection.',
    'Soulager': 'Méthodes pour soulager la douleur et l\'inconfort, telles que des compresses froides ou chaudes, ou des médicaments pour la douleur.',
    'Observations Exobuccales ( remarque generale ) ': 'Remarques générales sur les observations cliniques externes du patient, telles que la couleur de la peau, la présence d\'un gonflement ou d\'une rougeur, etc.'
    }

st.title("Predicting Emergencies in Dental Medicine")

# Loading classifiers trained in notebook
classifiers = {}
with open("GradientBoostingClassifier.pkl", 'rb') as f:
     classifiers["gradient boosting classifier"] = pkl.load(f)
    
with open("DecisionTreeClassifier.pkl", 'rb') as f:
     classifiers["Decision Tree Classifier"] = pkl.load(f)

with open("RandomForestClassifier.pkl", "rb") as f:
     classifiers["Random Forest Classifier"] = pkl.load(f)

# Loading Label Encoders
with open("label_encoders.pkl", "rb") as f:
     label_encoders = pkl.load(f)

with st.form("form"):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prenom")
    result = {}
    age = st.slider("Age Patient", min_value=1, max_value=100, step=1, value=44)
    for key, option in options.items():
        result[key] = st.selectbox(key, option, help=description[key] if 'Sexe' not in key else key)
    remarques = st.text_input("Remarque de docteur (optionelle)")
    see_data = st.checkbox("Voulez vous voir vos réponses ?")
    result = {"Prenom": prenom, "Nom": nom, "Age Patient": age, **result}
    predict_and_report = st.form_submit_button("Prediction")

# predict button is pressed
if predict_and_report:
        # if we want to see the data we're working on
        if see_data:
            st.write(result)
        features = np.array(features_from_form(result, label_encoders))
        predictions = {
            clf_name: label_encoders['Les Urgences En MED DENT'].inverse_transform(clf.predict(features.squeeze(1).reshape(1, -1))) 
            for clf_name, clf in classifiers.items()
                       }
        print(predictions)
        # getting the final prediction
        for clf, pred in predictions.items():
            st.write(f"## {clf}: {pred[0]}")
            
        # creating the report first into markdown then to html
        report = rapport_creator(result, predictions["Random Forest Classifier"][0], remarques)
        html = markdown_to_html(report)
        # Set the filename and content
        filename = f"{nom}_{prenom}.html"
        content = html.encode('utf-8')
        # Create a download link for the file
        href = f'<a href="data:application/octet-stream;base64,{b64encode(content).decode()}" download="{filename}">Click here to download</a>'
        st.markdown(href, unsafe_allow_html=True)
