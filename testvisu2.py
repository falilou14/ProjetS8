import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec

def read_file(filename):
    '''Lire les données à partir du fichier et les stocker dans un DataFrame'''
    data = []
    with open(filename, 'r') as file:
        for line in file:
            if 'CELL_' in line:
                parts = line.split(';')
                timestamp = parts[0]
                event = parts[1]
                details = parts[2]
                if 'newCharacter' in details:
                    char_info = details.split(',')
                    if len(char_info) >= 3:  # S'assurer qu'il y a assez de parties après la division
                        new_char = char_info[0].split('=')[1].strip().rstrip(',')
                        try:
                            x = int(char_info[1].split('=')[1].strip().rstrip(','))
                            y = int(char_info[2].split('=')[1].strip().rstrip(','))
                            data.append({'timestamp': timestamp, 'event': event, 'character': new_char, 'x': x, 'y': y})
                        except ValueError:
                            if 'CELL_' in line:
                                parts = line.split(';')
                                timestamp = parts[0]
                                event = parts[1]
                                details = parts[2]
                                if 'newCharacter' in details:
                                    char_info = details.split(',')
                                    if len(char_info) >= 4:
                                        # 2024-03-31T04:40:03.544Z;CELL_REPLACE;oldCharacter=L,newCharacter=I,x=10,y=3,
                                        new_char = char_info[1].split('=')[1].strip().rstrip(',')
                                        try:
                                            x = int(char_info[2].split('=')[1].strip().rstrip(','))
                                            y = int(char_info[3].split('=')[1].strip().rstrip(','))
                                            data.append({'timestamp': timestamp, 'event': event, 'character': new_char, 'x': x, 'y': y})
                                        except ValueError:
                                            print(f"Invalid coordinates in line: {line.strip()}")
                            else:
                            # Ignorer les lignes avec des coordonnées non valides
                                print(f"Invalid coordinates in line: {line.strip()}")
    return pd.DataFrame(data)

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

def create_heatmap_data(df, grid_size):
    #
    heatmap_data = np.zeros(grid_size)  # Initialiser la grille en fonction de la taille déterminée

    for _, row in df.iterrows():
        if 0 <= row['x'] < grid_size[0] and 0 <= row['y'] < grid_size[1]:  # Vérifier les limites de la grille
            if 'REPLACE' in row['event'] or 'INPUT' in row['event']:
                heatmap_data[row['x'], row['y']] += 1

    return heatmap_data

def calculate_average_non_zero(heatmap_data):
    non_zero_elements = heatmap_data[heatmap_data != 0]
    if non_zero_elements.size > 0:
        average = non_zero_elements.sum() / non_zero_elements.size
    else:
        average = 0
    return average

# Exemple d'utilisation
filename = '1711859764703.txt'  # Remplacez par le nom de votre fichier
df = read_file(filename)

# Convertir la colonne 'timestamp' en datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by='timestamp')

# Calculer la durée de la partie
start_time = df['timestamp'].min()
end_time = df['timestamp'].max()
duration_minutes = (end_time - start_time).total_seconds() / 60  # Durée en minutes
df['duration'] = (df['timestamp'] - start_time).dt.total_seconds() / 60  # Durée en minutes depuis le début

# Déterminer la taille de la grille en fonction des valeurs maximales de x et y
max_x = df['x'].max() + 1
max_y = df['y'].max() + 1
grid_size = (max_x, max_y)

# Créer les données de la heatmap
heatmap_data = create_heatmap_data(df, grid_size)

# Calculer la moyenne des cases non nulles
average_non_zero = calculate_average_non_zero(heatmap_data)

# Évaluation de la grille
celldiff, score = eval_grille(filename)

# Créer les visualisations
fig = plt.figure(figsize=(18, 10))
gs = GridSpec(2, 3, width_ratios=[3, 3, 1])

# Heatmap
ax1 = fig.add_subplot(gs[0, 0:2])
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", cbar=True, ax=ax1)
ax1.set_title("Heatmap of Character Insertions (including REPLACE)")
ax1.set_xlabel("Y Position")
ax1.set_ylabel("X Position")

# Timeline
ax2 = fig.add_subplot(gs[1, 0:2])
filtered_df = df[df['event'].str.contains('WRONG|CORRECT')]
filtered_df['event_numeric'] = filtered_df['event'].apply(lambda x: 0 if 'CORRECT' in x else 1)

ax2.scatter(filtered_df['duration'], filtered_df['event_numeric'], marker='o')
ax2.set_title("Timeline of Events")
ax2.set_xlabel("Duration (minutes)")
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['CORRECT', 'WRONG'])
ax2.grid(True)

# Colonne de données numériques
ax3 = fig.add_subplot(gs[:, 2])
ax3.axis('off')
textstr = '\n'.join((
    f'Average Non-Zero: {average_non_zero:.2f}',
    'Interprétation:',
    'Un score non-zero indique la moyenne des insertions',
    'effectuées dans les cellules qui ont été modifiées.',
    'Un score de 1 signifie un score parfait.',
    ''
    f'Number of Cells: {celldiff}',
    'Interprétation:',
    'Ce nombre représente le total des cellules',
    'différentes qui ont été modifiées.',
    '',
    f'Score: {score:.2f}%',
    'Interprétation:',
    'Le pourcentage de corrections réussies parmi',
    'toutes les tentatives (correctes et incorrectes).',
    '',
    f'Durée de la partie: {duration_minutes:.2f} minutes'
))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax3.text(0.4, 0.6, textstr, transform=ax3.transAxes, fontsize=12,
         verticalalignment='center', horizontalalignment='center', bbox=props)

plt.tight_layout()
plt.show()
