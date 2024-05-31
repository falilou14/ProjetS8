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
    #conn.row_factory = sqlite3.Row  # Pour que les résultats de requête soient sous forme de dictionnaires
    return conn
    return conn

################################################## SERVICES POUR LA TABLE USER ######################################################

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



@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    id_user = data.get("id")
    nom = data.get("nom")
    prenom = data.get("prenom")
    adresse_mail = data.get('email')
    tel = data.get("tel")
    password = data.get('password')
    username = data.get('username')

    # Vérifier si l'utilisateur existe déjà
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE adresse_mail = ? OR username = ?", (adresse_mail, username))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({'error': 'L\'utilisateur existe déjà'}), 400

    # Insérer l'utilisateur dans la base de données
    cursor.execute("INSERT INTO user (id_user, nom, prenom, adresse_mail, tel, mot_de_passe, username) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (id_user, nom, prenom, adresse_mail, tel, password, username))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Utilisateur inscrit avec succès'}), 201


# Endpoint pour la connexion
@app.route('/login', methods=['POST'])
def login():
    '''
    Fonction login .....
    '''
    data = request.get_json()
    adresse_mail = data.get('email')
    password = data.get('password')

    # Rechercher l'utilisateur dans la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE adresse_mail = ? AND mot_de_passe = ?", (adresse_mail, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Connexion réussie', 'user': user}), 200
    else:
        return jsonify({'error': 'Utilisateur non trouvé ou mot de passe incorrect'}), 401
    





############################################## SERVICES POUR LA TABLE THEMES ######################################################

#Endpoint pour ajouter un theme 
@app.route('/addTheme', methods=['POST'])
def AddTheme ():
    data = request.get_json()
    username = data.get('username')
    intitule = data.get('intitule')
    list_q = data.get('list_q')
    
    # Vérifier si l'utilisateur existe
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    conn.close()
    
    if not existing_user:
        return jsonify({'error': 'Nom d\'utilisateur invalide'}), 400

    # Vérifier si le thème existe déjà
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM theme WHERE intitule = ? OR list_q = ?", (intitule, list_q))
    existing_theme = cursor.fetchone()
    conn.close()

    if existing_theme:
        return jsonify({'error': 'Le thème existe déjà'}), 400

    # Ajouter le nouveau thème dans la base de données 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO theme (intitule, list_q) VALUES (?, ?)", (intitule, list_q))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Thème ajouté avec succès'}), 201

       
           


#endpoint pour mettre à jour un Theme 
@app.route('/UpdateTheme', methods=['POST'])
def UpdateTheme():
    data = request.get_json()
    id_user = data.get('id')
    intitule = data.get('intitule')
    new_intitule = data.get('new_intitule')
    new_list_q = data.get('new_list_q')

    # Vérifier si l'utilisateur existe
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id_user = ?", (id_user,))
    existing_user = cursor.fetchone()

    if not existing_user:
        conn.close()
        return jsonify({'error': 'L\'utilisateur n\'existe pas'}), 404

    # Vérifier si le thème existe
    cursor.execute("SELECT * FROM theme WHERE intitule = ?", (intitule,))
    existing_theme = cursor.fetchone()

    if not existing_theme:
        conn.close()
        return jsonify({'error': 'Le thème n\'existe pas'}), 404

    # Mettre à jour le thème en fonction de son id_theme
    id_theme = existing_theme[0]  # Récupérer l'id_theme du thème existant
    cursor.execute("UPDATE theme SET intitule = ?, list_q = ? WHERE id_theme = ?",
                   (new_intitule, new_list_q, id_theme))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Thème mis à jour avec succès'}), 200

    
############################################## SERVICES POUR LA TABLE EVENNEMENT ##############################################


#Ici on redéfini notre fonction de connexion à la base de données pour que les résultats de requête soient sous forme de dictionnaires
def get_db_connection_event():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Pour que les résultats de requête soient sous forme de dictionnaires
    return conn
    

# Endpoint pour ajouter un événement
@app.route('/addEvent', methods=['POST'])
def add_event():
    data = request.get_json()
    username = data.get('username')
    nom_grille = data.get('nom_grille')
    nom_style = data.get('nom_style')
    date_debut = data.get('date_debut')
    date_fin = data.get('date_fin')

    # Vérifier si l'utilisateur existe
    conn = get_db_connection_event()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if not existing_user:
        conn.close()
        return jsonify({'error': 'Utilisateur non existant'}), 404

    # Trouver l'ID de la grille à partir de son nom
    cursor.execute("SELECT id_grille FROM grille_jeu WHERE nom_grille = ?", (nom_grille,))
    grille = cursor.fetchone()

    if not grille:
        conn.close()
        return jsonify({'error': 'Grille non trouvée'}), 404

    id_grille = grille['id_grille']

    # Trouver l'ID du style à partir de son nom
    cursor.execute("SELECT id_style FROM style WHERE nom_style = ?", (nom_style,))
    style = cursor.fetchone()

    if not style:
        conn.close()
        return jsonify({'error': 'Style non trouvé'}), 404

    id_style = style['id_style']

    # Vérifier si un événement similaire existe déjà
    cursor.execute("SELECT * FROM evennement_jeu WHERE id_grille = ? AND id_style = ? AND date_debut = ? AND date_fin = ?",
                   (id_grille, id_style, date_debut, date_fin))
    existing_event = cursor.fetchone()

    if existing_event:
        conn.close()
        return jsonify({'error': 'L\'événement existe déjà'}), 400

    # Ajouter le nouvel événement dans la base de données
    cursor.execute("INSERT INTO evennement_jeu (id_grille, id_style, date_debut, date_fin) VALUES (?, ?, ?, ?)",
                   (id_grille, id_style, date_debut, date_fin))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Événement ajouté avec succès'}), 201




# Endpoint pour mettre à jour un événement
@app.route('/updateEvent', methods=['POST'])
def update_event():
    data = request.get_json()
    username = data.get('username')
    id_event = data.get('id_event')
    new_nom_style = data.get('new_nom_style')
    new_date_debut = data.get('new_date_debut')
    new_date_fin = data.get('new_date_fin')

    # Vérifier si l'utilisateur existe
    conn = get_db_connection_event()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if not existing_user:
        conn.close()
        return jsonify({'error': 'Utilisateur non existant'}), 404

    # Vérifier si l'événement existe
    cursor.execute("SELECT * FROM evennement_jeu WHERE id_event = ?", (id_event,))
    existing_event = cursor.fetchone()

    if not existing_event:
        conn.close()
        return jsonify({'error': 'L\'événement n\'existe pas'}), 404

    # Vérifier si le style existe
    cursor.execute("SELECT id_style FROM style WHERE nom_style = ?", (new_nom_style,))
    style = cursor.fetchone()

    if not style:
        conn.close()
        return jsonify({'error': 'Le style n\'existe pas'}), 404

    # Mettre à jour l'événement
    id_style = style['id_style']
    update_fields = []
    update_values = []

    if new_nom_style:
        update_fields.append("id_style = ?")
        update_values.append(id_style)
    if new_date_debut:
        update_fields.append("date_debut = ?")
        update_values.append(new_date_debut)
    if new_date_fin:
        update_fields.append("date_fin = ?")
        update_values.append(new_date_fin)

    if update_fields:
        update_values.append(id_event)
        cursor.execute(f"UPDATE evennement_jeu SET {', '.join(update_fields)} WHERE id_event = ?", update_values)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Événement mis à jour avec succès'}), 200
    else:
        conn.close()
        return jsonify({'message': 'Aucune mise à jour fournie'}), 400



############################################## SERVICES POUR LA TABLE JEU ##############################################


# Endpoint pour ajouter un jeu
@app.route('/addGame', methods=['POST'])
def addGame():
    data = request.get_json()
    nom_jeu = data.get('nom_jeu')
    id_theme = data.get('id_theme')
    difficultes = data.get('difficultes')

    # Ajouter le nouveau jeu dans la base de données 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jeu (nom_jeu, id_theme, difficultes) VALUES (?, ?, ?)", 
                   (nom_jeu, id_theme, difficultes))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Jeu ajouté avec succès'}), 201















    

if __name__ == '__main__':
    app.run(debug=True)
