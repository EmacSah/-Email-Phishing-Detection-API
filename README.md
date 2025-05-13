🔒 Email Phishing Detection API

Une application web sécurisée qui utilise le machine learning pour détecter les emails de phishing en temps réel avec une précision de 97%.

🌟 Fonctionnalités

Détection par ML: Classification de texte d'emails avec vectorisation TF-IDF et régression logistique
API sécurisée: Authentification par clé d'API et chiffrement des données sensibles
Interface web: Interface utilisateur intuitive pour tester la détection de phishing
Protection multicouche: Authentification, chiffrement, et communications HTTPS

📋 Architecture du projet
L'application est structurée selon une architecture modulaire et sécurisée:
/
├── app.py                # Application Flask principale
├── models/               # Modèles ML préentraînés
│   ├── phishing_model.pkl       # Modèle entraîné pour la détection
│   └── tfidf_vectorizer.pkl     # Vectoriseur TF-IDF préentraîné
├── templates/            # Templates Flask
│   └── index.html              # Interface utilisateur principale
├── static/               # Ressources statiques (CSS, JS, images)
├── keys/                 # Clés de chiffrement (non exposées)
└── requirements.txt      # Dépendances du projet
🔧 Technologies

- Backend: Python 3.x, Flask
- ML: scikit-learn, pandas, TF-IDF vectorization
- Sécurité: Fernet (chiffrement), Authentication par clé API
- Frontend: HTML, CSS, JavaScript
- Déploiement: ngrok (tunneling HTTPS)

🛡️ Mesures de sécurité

Authentification de l'API

- Implémentation d'un système de clé API via headers HTTP (X-API-Key)
- Mécanisme de vérification par décorateur Flask sur les endpoints sensibles
- Proxy côté serveur pour éviter l'exposition des clés d'API au client

Chiffrement des données

- Utilisation de Fernet pour le chiffrement symétrique des données sensibles
- Stockage sécurisé des clés de chiffrement via variables d'environnement
- Protection des données au repos et en transit

Sécurisation des communications

- Tunnel HTTPS via ngrok pour toutes les communications
- En-têtes de sécurité HTTP pour prévenir les attaques courantes
- Isolation des ressources sensibles

📊 Performance du modèle

Métrique                                                Valeur   
---------------------------------------------------------------
Précision - Classe 0 (Safe)                              98%
Précision - Classe 1 (Phishing)                          95%
Rappel - Classe 0 (Safe)                                 96%
Rappel - Classe 1 (Phishing)                             97%
Score F1 Global                                          97%
AUC-ROC                                                 0.97

------------------------------------------------------------------------------------------------------------------------------------------------------------------
🚀 Installation et déploiement

Prérequis

- Python 3.7+
- Compte ngrok pour le tunneling HTTPS
- Bibliothèques Python (voir requirements.txt)

Configuration

- Cloner ce dépôt :
bashgit clone https://github.com/emacsah/email-phishing-detection.git
cd email-phishing-detection

- Installer les dépendances : bashpip install -r requirements.txt

- Configurer les variables d'environnement

  - bashexport API_KEY="votre_clé_api_secrète"
  - export FERNET_KEY="votre_clé_fernet_générée"

- Exécuter l'application : bashpython app.py

📝 Guide d'utilisation

- Accéder à l'interface web via l'URL générée par ngrok
- Saisir le contenu de l'email à analyser dans le champ de texte
- Cliquer sur "Prédire" pour lancer l'analyse
- Le résultat de la prédiction s'affiche (Safe Email ou Phishing Email)

🔍 API Endpoints

- GET / - Page d'accueil avec interface utilisateur
- POST /predict - Endpoint principal pour la prédiction (nécessite X-API-Key)
- POST /submit_email - Proxy sécurisé pour les clients web (ne nécessite pas X-API-Key)

🛠️ Évolutions futures

- Implémentation d'une authentification par token JWT pour plus de sécurité
- Ajout d'un système de logging sécurisé pour l'audit des prédictions
- Mise en place d'un pipeline CI/CD pour le déploiement automatisé
- Containerisation avec Docker pour faciliter le déploiement
- Extension du modèle pour détecter d'autres types de menaces

📜 Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
