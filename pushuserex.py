from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bdd3 import User, Groupe  # Supposons que vous avez défini vos classes de modèle dans un fichier models.py

# Créer le moteur de la base de données
engine = create_engine('sqlite:///jeux_database.db', echo=True)  # Changez sqlite:///jeux_database.db par votre URL de base de données

# Créer une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Créer des instances d'objets à insérer dans la base de données
user1 = User( id_user='65b3ab25378634a66d2afb4c',nom='John', prenom='Doe', adresse_mail='john.doe@example.com', tel='123456789', mot_de_passe='password123',username='quafafou')



# Ajouter les instances à la session
session.add(user1)


# Committer les changements pour les sauvegarder dans la base de données
session.commit()

# Fermer la session
session.close()
