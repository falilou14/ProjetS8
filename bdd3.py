from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Créer le moteur de la base de données
engine = create_engine('sqlite:///jeux_database.db', echo=True)  # Changez sqlite:///jeux_database.db par votre URL de base de données

# Déclarer une base pour définir les classes de modèle
Base = declarative_base()

# Définir les classes de modèle pour chaque table
class User(Base):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    adresse_mail = Column(String)
    tel = Column(String)
    mot_de_passe = Column(String)
    username = Column(String)
    role = Column(String)

#Composé de users
class Groupe(Base):
    __tablename__ = 'groupe'

    id_groupe = Column(Integer, primary_key=True)
    nom_groupe = Column(String)
    liste_id_users = Column(String)  # Peut-être une liste d'ids sérialisée

#composé de users
class Team(Base):
    __tablename__ = 'team'

    id_team = Column(Integer, primary_key=True)
    nom_team = Column(String)
    liste_id_users = Column(String)
    id_challenge = Column(Integer)

#theme du jeu (c++, python, java, poo, algo, etc)
class Theme(Base):
    __tablename__ = 'theme'

    id_theme = Column(Integer, primary_key=True)
    intitule = Column(String)
    list_q = Column(String)  # Peut-être une liste de triplets sérialisée
    DateCreation = Column(String)
    id_theme_owner = Column(Integer)

class Jeu(Base):
    __tablename__ = 'jeu'

    id_jeu = Column(Integer, primary_key=True)
    nom_jeu = Column(String)
    id_theme = Column(Integer)
    difficultes = Column(String)
    AssistanceMode =Column(String)  # Peut-être une liste de difficultés sérialisée
    DateCreation = Column(String)

#grille sur lequel le jeu est joué
class GrilleJeu(Base):
    __tablename__ = 'grille_jeu'

    id_grille = Column(Integer, primary_key=True)
    nom_grille = Column(String)
    id_jeu = Column(Integer)
    root_grille = Column(String)

class EvennementJeu(Base):
    __tablename__ = 'evennement_jeu'

    id_event = Column(Integer, primary_key=True)
    id_grille = Column(Integer, ForeignKey('grille_jeu.id_grille'))
    id_style = Column(String)
    date_debut = Column(String)
    date_fin = Column(String)
    eventProperty = Column(String)  


class JeuJouer(Base):
    __tablename__ = 'jeu_jouer'

    id_jeu_jouer = Column(Integer, primary_key=True)
    id_event = Column(Integer, ForeignKey('evennement_jeu.id_event'))
    log = Column(String)
    list = Column(String)  # Peut-être une liste de tuples (secret du jeu, eval) sérialisée
    eval_grille = Column(String)

#type d'evenement (tournoi,challenge, 1v1)
class Style(Base):
    __tablename__ = 'style'

    id_style = Column(Integer, primary_key=True)
    nom_style = Column(String)
    liste_id_participants = Column(String)  # Peut-être une liste d'ids sérialisée
# Créer les tables dans la base de données
Base.metadata.create_all(engine)
