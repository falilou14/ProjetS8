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
file_path = '1711859764703.txt'
nb_cellules_differentes, score = eval_grille(file_path)
print(f'Nombre de cellules différentes: {nb_cellules_differentes}')
print(f'Score: {score:.2f}%')

# nbcel,score=eval_grille(event) 
