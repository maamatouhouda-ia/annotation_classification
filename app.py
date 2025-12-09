import streamlit as st
import os
from PIL import Image
import pandas as pd
from datetime import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="Annotation d'images",
    page_icon="🔍",
    layout="centered"
)

# Liste complète des questions - REMPLACEZ PAR VOS DONNÉES COMPLÈTES
data = [
    {'image': '20250327_143847_400000_004306_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'},
    {'image': '20250327_155806_700000_006074_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'},
    {'image': '20250327_155806_700000_009723_2.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'},
    {'image': '20250612_090537_gx010001_f_2580_photo_3.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'},
    {'image': '20250612_091811_gx010002_f_9686_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'},
    {'image': 'Abedul_Arriere_no_name_20241012_110117_001_001481_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'},
    # ... AJOUTEZ TOUTES VOS DONNÉES ICI
]

# Filtrer pour garder seulement les erreurs de prédiction
questions = [item for item in data if item['label'] != item['prediction']]

# Initialisation de la session
if "responses" not in st.session_state:
    st.session_state.responses = {}
    for i, q in enumerate(questions):
        st.session_state.responses[i] = {
            "label_choisi": "",
            "commentaire": ""
        }

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "annotator_name" not in st.session_state:
    st.session_state.annotator_name = ""

if "started" not in st.session_state:
    st.session_state.started = False

# Fonction de sauvegarde
def save_responses():
    """Sauvegarde les réponses dans un fichier JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        "annotateur": st.session_state.annotator_name,
        "date": timestamp,
        "annotations": []
    }
    
    for i, q in enumerate(questions):
        results["annotations"].append({
            "image": q["image"],
            "label_original": q["label"],
            "prediction_modele": q["prediction"],
            "label_choisi": st.session_state.responses[i]["label_choisi"],
            "commentaire": st.session_state.responses[i]["commentaire"]
        })
    
    return results

# CSS personnalisé
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #00cc66;
    }
    .big-font {
        font-size: 1.2rem !important;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Interface principale
st.title("🔍 Annotation d'images - Contrôle qualité")
st.markdown("---")

# Écran de démarrage
if not st.session_state.started:
    st.markdown("""
    ### Bienvenue dans l'outil d'annotation
    
    Ce formulaire vous permet de vérifier et corriger les prédictions du modèle d'IA.
    
    **Instructions:**
    - Vous verrez des images où le modèle a fait une prédiction différente du label original
    - Pour chaque image, confirmez le bon label
    - Ajoutez un commentaire si nécessaire
    - Vos réponses seront automatiquement sauvegardées à la fin
    """)
    
    name = st.text_input("Votre nom/prénom:", key="name_input")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 Commencer l'annotation", type="primary", use_container_width=True):
            if name.strip():
                st.session_state.annotator_name = name.strip()
                st.session_state.started = True
                st.rerun()
            else:
                st.error("⚠️ Veuillez entrer votre nom")
    
    st.info(f"📊 Nombre total d'images à annoter: **{len(questions)}**")
    
    # Section info
    with st.expander("ℹ️ Informations complémentaires"):
        st.markdown("""
        **Catégories disponibles:**
        - `faiencage`: Réseau de fissures fines
        - `fissure_degradee`: Fissure avec dégradation
        - `fissure_significative`: Fissure importante
        - `joint_ouvert`: Joint ouvert visible
        
        **Temps estimé:** ~{} minutes ({}s par image)
        """.format(len(questions) // 2, 30))

else:
    # Interface d'annotation
    q_idx = st.session_state.current_question
    
    # Vérifier si on a terminé
    if q_idx >= len(questions):
        st.success("🎉 **Annotation terminée !**")
        st.balloons()
        
        # Résumé
        st.markdown("### 📊 Résumé de vos annotations")
        
        results_data = save_responses()
        
        results_list = []
        for annotation in results_data["annotations"]:
            results_list.append({
                "Image": annotation["image"],
                "Label original": annotation["label_original"],
                "Prédiction IA": annotation["prediction_modele"],
                "Votre choix": annotation["label_choisi"],
                "Commentaire": annotation["commentaire"]
            })
        
        df = pd.DataFrame(results_list)
        st.dataframe(df, use_container_width=True)
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        with col1:
            agree_with_original = sum(1 for r in results_data["annotations"] if r["label_choisi"] == r["label_original"])
            st.metric("Accord label original", f"{agree_with_original}/{len(questions)}")
        with col2:
            agree_with_model = sum(1 for r in results_data["annotations"] if r["label_choisi"] == r["prediction_modele"])
            st.metric("Accord prédiction IA", f"{agree_with_model}/{len(questions)}")
        with col3:
            other_labels = sum(1 for r in results_data["annotations"] if r["label_choisi"] not in [r["label_original"], r["prediction_modele"]])
            st.metric("Autres labels", other_labels)
        
        # Boutons de téléchargement
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name=f"annotations_{st.session_state.annotator_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            json_str = json.dumps(results_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Télécharger JSON",
                data=json_str,
                file_name=f"annotations_{st.session_state.annotator_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        if st.button("🔄 Faire une nouvelle annotation", use_container_width=True):
            st.session_state.started = False
            st.session_state.current_question = 0
            st.session_state.responses = {}
            st.rerun()
    
    else:
        question = questions[q_idx]
        
        # Barre de progression
        progress = (q_idx) / len(questions)
        st.progress(progress)
        st.caption(f"Image {q_idx + 1} sur {len(questions)}")
        
        # Informations sur l'annotateur
        col_info1, col_info2 = st.columns([3, 1])
        with col_info1:
            st.markdown(f"**Annotateur:** {st.session_state.annotator_name}")
        with col_info2:
            if st.button("🏠 Accueil"):
                st.session_state.started = False
                st.rerun()
        
        st.markdown("---")
        
        # Affichage de l'image
        label = question['label']
        image_name = question["image"]
        image_path = os.path.join("test", label, image_name)
        
        # Essayer différents chemins si l'image n'est pas trouvée
        if not os.path.exists(image_path):
            # Essayer sans le dossier label
            image_path = os.path.join("test", image_name)
            if not os.path.exists(image_path):
                # Essayer directement le nom
                image_path = image_name
        
        col_img, col_info = st.columns([2, 1])
        
        with col_img:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                st.image(img, use_column_width=True)
            else:
                st.warning(f"⚠️ Image non trouvée localement")
                st.info(f"📁 Chemin attendu: `{image_path}`")
                st.markdown("""
                **Note:** En mode déploiement, assurez-vous que les images 
                sont bien dans le dossier `test/` de votre repository GitHub.
                """)
        
        with col_info:
            st.markdown("### 📋 Informations")
            st.markdown(f"**Fichier:**")
            st.code(image_name, language=None)
            st.markdown(f"**Label original:**  \n`{question['label']}`")
            st.markdown(f"**Prédiction IA:**  \n`{question['prediction']}`")
        
        st.markdown("---")
        
        # Zone d'annotation
        st.markdown("### ✏️ Votre annotation")
        
        # Choix du label
        labels_disponibles = [question["label"], question["prediction"], "Autre"]
        
        # Gérer l'index par défaut
        current_choice = st.session_state.responses[q_idx]["label_choisi"]
        if current_choice in labels_disponibles:
            default_index = labels_disponibles.index(current_choice)
        elif current_choice != "":
            default_index = 2  # "Autre"
        else:
            default_index = 0
        
        choice = st.radio(
            "Quel est le **bon label** pour cette image ?",
            labels_disponibles,
            key=f"question_{q_idx}",
            index=default_index
        )
        
        # Champ texte si "Autre" est choisi
        if choice == "Autre":
            new_label = st.text_input(
                "Précisez le nouveau label:",
                key=f"new_label_{q_idx}",
                value=st.session_state.responses[q_idx]["label_choisi"] 
                      if st.session_state.responses[q_idx]["label_choisi"] not in labels_disponibles 
                      else "",
                placeholder="Ex: fissure_longitudinale"
            )
            st.session_state.responses[q_idx]["label_choisi"] = new_label if new_label else ""
        else:
            st.session_state.responses[q_idx]["label_choisi"] = choice
        
        # Commentaire optionnel
        comment = st.text_area(
            "Commentaire (optionnel):",
            key=f"comment_{q_idx}",
            value=st.session_state.responses[q_idx]["commentaire"],
            placeholder="Ex: L'image est floue, difficile à classifier...",
            height=100
        )
        st.session_state.responses[q_idx]["commentaire"] = comment
        
        st.markdown("---")
        
        # Boutons de navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⬅️ Précédent", disabled=(q_idx == 0), use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
        
        with col2:
            # Vérifier si une réponse a été donnée
            has_response = st.session_state.responses[q_idx]["label_choisi"] != ""
            if not has_response:
                st.warning("⚠️ Veuillez choisir un label avant de continuer")
        
        with col3:
            button_label = "Suivant ➡️" if q_idx < len(questions) - 1 else "✅ Terminer"
            if st.button(button_label, type="primary", disabled=not has_response, use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    Outil d'annotation - Version 1.0 | Développé avec Streamlit
</div>
""", unsafe_allow_html=True)