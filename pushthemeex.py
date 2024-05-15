from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Création de la classe de base pour les déclarations de la table
Base = declarative_base()

# Définition de la classe Theme
class Theme(Base):
    __tablename__ = 'theme'

    id_theme = Column(Integer, primary_key=True)
    intitule = Column(String)
    list_q = Column(String)  # Peut-être une liste de triplets sérialisée

# Création d'un moteur SQLAlchemy
engine = create_engine('sqlite:///jeux_database.db', echo=True)  

# Création des tables dans la base de données
Base.metadata.create_all(engine)

# Création d'une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Insertion des données
themes_data = ["linux", "c++", "c#", "java", "python", "poo", "algo"]

for theme_name in themes_data:
    # Vérifier si le thème existe déjà dans la base de données
    existing_theme = session.query(Theme).filter_by(intitule=theme_name).first()
    if existing_theme is None:
        # Si le thème n'existe pas, l'ajouter
        theme = Theme(intitule=theme_name)
        session.add(theme)

try:
    # Exécuter les transactions
    session.commit()
except IntegrityError:
    # Gérer les erreurs d'intégrité si les données sont déjà présentes
    session.rollback()
finally:
    # Fermer la session
    session.close()