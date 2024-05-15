from flask import Flask, request, jsonify
import sqlite3




#######################################"" TEST ######################################

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'



# Chemin vers la base de données SQLite
DATABASE_PATH = 'jeux_database.db'

# Fonction pour se connecter à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn



# Endpoint pour afficher tous les noms des utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Username , id_user , prenom  FROM user")
    users = cursor.fetchall()
    conn.close()

    users_data = [{'id_user': user[1], 'username': user[0], 'firstname': user[2]} for user in users]
   
    return jsonify({'users': users_data}), 200





# Endpoint pour l'inscription
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    nom = data.get("nom")
    prenom = data.get(prenom)
    adresse_mail = data.get('email')
    password = data.get('password')
    username = data.get('username')

    # Insérer l'utilisateur dans la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User ( nom, prenom ,adresse_mail, password ,username,) VALUES (?, ?, ?)", ( nom, prenom,adresse_mail, password,username,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Utilisateur inscrit avec succès'}), 201

# Endpoint pour la connexion
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    adresse_mail = data.get('email')
    password = data.get('password')

    # Rechercher l'utilisateur dans la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE adresse_mail = ? AND password = ?", (adresse_mail, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Connexion réussie', 'user': user}), 200
    else:
        return jsonify({'error': 'Utilisateur non trouvé ou mot de passe incorrect'}), 401
    
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
