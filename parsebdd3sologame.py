import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bdd3 import User,Groupe,Team,Theme,Jeu,GrilleJeu,EvennementJeu,Style,JeuJouer  

# Créer le moteur de la base de données
engine = create_engine('sqlite:///jeux_database.db', echo=True)  # Changez sqlite:///jeux_database.db par votre URL de base de données

# Créer une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

filename = '1711859764703.txt'

def eval_grille(file_path):
    # Utilisation de sets pour garder les coordonnées uniques
    cellules_differentes = set()
    correct_count = 0
    wrong_count = 0
    
    # Lecture du fichier ligne par ligne
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            event_type = parts[1]
            if event_type in ['CELL_INPUT', 'CELL_CORRECT', 'CELL_WRONG', 'CELL_REPLACE']:
                # Extraction des coordonnées x et y
                coord_str = parts[2]  # Par exemple: 'x=0,y=7'
                coord_parts = coord_str.split(',')
                x = coord_parts[1].split('=')[1]
                y = coord_parts[2].split('=')[1]
                coord = (x, y)
                cellules_differentes.add(coord)
            
            if event_type == 'CELL_CORRECT':
                correct_count += 1
            elif event_type == 'CELL_WRONG':
                wrong_count += 1
    
    # Nombre de cellules différentes
    nb_cellules_differentes = len(cellules_differentes)
    
    # Calcul de la performance
    total_attempts = correct_count + wrong_count
    if total_attempts == 0:
        score = 0
    else:
        score = correct_count / total_attempts * 100
    
    return nb_cellules_differentes, score

# Exemple d'utilisation avec un fichier 'events.txt'

def getlog(filename):
    with open(filename, 'r') as file:
    # Lire toutes les lignes du fichier
        lines = file.readlines()
        chaine_unique = ''.join(lines[1:])
        return chaine_unique

def getdateevent(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        horodatages = []
        for line in [lines[1], lines[-1]]:
            timestamp = line.strip().split(';')[0]
           
            horodatages.append(timestamp)
    
    print("Horodatages (time stamps):", horodatages)
    return horodatages

def parse_first_line(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip()
        parts = first_line.split(';')
        if len(parts) == 8:
            UserId = parts[0]
            Username = parts[1]
            theme = parts[2]
            difficulty = parts[3]
            AssistanceMode = parts[4]
            grilleID = filename
            grilleID = filename.split('.')[0]
            return UserId, Username, theme, difficulty, grilleID,AssistanceMode
    return "UserIdNotFound", "UsernameNotFound", "ThemeNotFound", "DifficultyNotFound", "GrilleIDNotFound","AssistanceModeNotFound"

def verify_log(UserId,Username,theme):
    existing_user = session.query(User).filter_by(id_user=UserId).first()
    existing_theme = session.query(Theme).filter_by(intitule=theme).first()

    if not existing_user:
        print(f"L'utilisateur '{Username}' n'existe pas dans la base de données.")
        sys.exit("Arrêt du programme : L'utilisateur spécifié n'existe pas dans la base de données.")

    if not existing_theme:
        print(f"Le thème '{theme}' n'existe pas dans la base de données.")
        sys.exit("Arrêt du programme : Le thème spécifié n'existe pas dans la base de données.")


UserId,Username,theme,difficulty,grilleID,AssistanceMode=parse_first_line(filename)

nb_cellules_differentes, score = eval_grille(filename)
print(f'Nombre de cellules différentes: {nb_cellules_differentes}')
print(f'Score: {score:.2f}%')

existing_theme = session.query(Theme).filter_by(intitule=theme).first()
#ajout de "Jeu" dans la base de données
id_theme = existing_theme.id_theme
jeu=Jeu(nom_jeu='jsp',id_theme=id_theme,difficultes=difficulty,AssistanceMode=AssistanceMode)
session.add(jeu)
session.commit()
#ajout de "GrilleJeu" dans la base de données
grille_jeu = GrilleJeu(id_grille=grilleID,nom_grille='jsp',id_jeu=jeu.id_jeu,root_grille='jsp')
session.add(grille_jeu)
session.commit()
#ajout de "Style" dans la base de données
style=Style(nom_style='solo',liste_id_participants=UserId)
session.add(style)
session.commit()
#ajout de "EvennementJeu" dans la base de données
date=getdateevent(filename)
evenementjeu=EvennementJeu(id_grille=grilleID,id_style=style.id_style,date_debut=date[0],date_fin=date[1],eventProperty='afaire')
session.add(evenementjeu)
session.commit()
#ajout de "JeuJouer" dans la base de données
log=getlog(filename)
jeu_jouer=JeuJouer(id_event=evenementjeu.id_event,log=log,list='jsp',eval_grille=score)

# Ajouter les instances à la session
session.add(jeu_jouer)
session.commit()

# Committer les changements pour les sauvegarder dans la base de données


# # Fermer la session
# session.close()
