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
    id_user = data.get('id')
    intitule = data.get('intitule')
    list_q = data.get('list_q')
    # Vérifier si l'id_user est valide pour pouvoir ajouter un theme :
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id_user = ? ", (id_user,))
    existing_user = cursor.fetchone()
    
    if(not existing_user):
        
        conn.close()
        return jsonify({'error': 'id no existant '})
    
    if existing_user:
       cursor.execute("SELECT * FROM theme WHERE intitule = ? OR list_q = ?", (intitule, list_q))
       existing_theme = cursor.fetchone()
       #si le theme existe déjà :
       if existing_theme:
           conn.close()
           return jsonify({'error': 'Le theme existe déjà'}), 400
       
       #sinon:On peut ajouter le nouveau theme dans la base de données 
       cursor.execute("INSERT INTO theme (intitule , list_q) VALUES (?,?) ",(intitule,list_q))
       conn.commit()
       conn.close()
       
       return jsonify({'message': 'Theme ajouté avec succès'}), 201
       
           

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

    















    

if __name__ == '__main__':
    app.run(debug=True)
