
from flask import Flask, request, jsonify, render_template
from langdetect import detect
from cryptography.fernet import Fernet
import pickle
import os
import re
import requests
from pyngrok import ngrok
from functools import wraps


#---------- Charger la clé Fernet depuis la variable d'environnement -------------

FERNET_KEY_ENV_VAR = 'FERNET_KEY'
fernet_key_raw = os.environ.get(FERNET_KEY_ENV_VAR)
cipher_suite = None
if fernet_key_raw:
    try:
        fernet_key = fernet_key_raw.encode('utf-8')
        cipher_suite = Fernet(fernet_key)
        print("Clé Fernet chargée depuis la variable d'environnement (dans cryp).")
    except Exception as e:
        print(f"Erreur lors du chargement de la clé Fernet depuis l'environnement (dans cryp) : {e}")
else:
    print("Erreur : La variable d'environnement FERNET_KEY n'est pas définie (dans cryp).")


#-------- GESTION DE LA CLÉ D'API --------------------------------------------------

API_KEY_ENV_VAR = 'API_KEY'
API_KEY = os.environ.get(API_KEY_ENV_VAR)
if not API_KEY:
    API_KEY = secrets.token_hex(32)
    os.environ[API_KEY_ENV_VAR] = API_KEY # Temporaire pour cet exemple en Colab
    print(f"Clé API générée et stockée (temporairement dans l'environnement) : {API_KEY}")
else:
    print(f"Clé API chargée depuis l'environnement.")


#-------- DÉCORATEUR POUR L'AUTHENTIFICATION ---------------------------------------

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('X-API-Key')
        if auth_header and auth_header == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Authentification requise"}), 401
    return decorated_function

#-----------------------------------------------------------------------------------

app = Flask(__name__,
            template_folder='/content/drive/MyDrive/cybersecurite/Cyberproject/templates',
            static_folder='/content/drive/MyDrive/cybersecurite/Cyberproject/static')

# Chemin vers les fichiers du modèle et du vectoriseur dans Google Drive
MODEL_PATH = '/content/drive/MyDrive/cybersecurite/Cyberproject/models/phishing_model.pkl'
VECTORIZER_PATH = '/content/drive/MyDrive/cybersecurite/Cyberproject/models/tfidf_vectorizer.pkl'

model = None
vectorizer = None

def load_model_and_vectorizer():
    global model
    global vectorizer
    try:
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
        with open(VECTORIZER_PATH, 'rb') as file:
            vectorizer = pickle.load(file)
        print("Modèle et vectoriseur chargés avec succès.")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle ou du vectoriseur : {e}")

load_model_and_vectorizer()


#----- bloc de code ajouté /submit_email -------------------------------------------------

@app.route('/submit_email', methods=['POST'])
def submit_email():
    data = request.get_json()
    if not data or 'email_content' not in data:
        return jsonify({"error": "Champ 'email_content' manquant dans la requête."}), 400

    email_content = data['email_content']
    headers = {'Content-Type': 'application/json', 'X-API-Key': API_KEY}
    predict_url = request.url_root + 'predict' # Construire l'URL complète de /predict

    try:
        response = requests.post(predict_url, headers=headers, json={'email_content': email_content})
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erreur lors de la communication avec l'API de prédiction: {e}"}), 500

#--------------fin de bloc de code --------------------------------------------------------------------



@app.route('/')
def index():
    return render_template('index.html', API_KEY=API_KEY)

@app.route('/predict', methods=['POST'])
@require_auth
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": "Le modèle ou le vectoriseur n'a pas pu être chargé."}), 500

    data = request.get_json()
    if not data or 'email_content' not in data:
        return jsonify({"error": "Champ 'email_content' manquant dans la requête."}), 400

    email_content = data['email_content'].strip()
    if not email_content:
        return jsonify({"error": "Contenu de l'e-mail vide."}), 400

    if not re.search(r'[a-zA-Z]', email_content):
        return jsonify({"error": "Le contenu de l'e-mail doit contenir des caractères anglais."}), 400

    try:
        language = detect(email_content)
        if language != 'en':
            return jsonify({"error": "Le contenu de l'e-mail doit être en anglais."}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la détection de la langue: {e}"}), 400

    email_vectorized = vectorizer.transform([email_content])
    prediction = model.predict(email_vectorized)[0]
    result = "Phishing Email" if prediction == 1 else "Safe Email"
    return jsonify({"prediction": result})

if __name__ == '__main__':
    # Set up ngrok tunnel
    public_url = ngrok.connect(5000)
    print("Public URL:", public_url)

    # Run app
    app.run(port=5000)
