# Fonction pour transformer la liste de dictionnaires en une liste de tuples
def transform_data(data):
    transformed_data = []
    for item in data:
        timestamp = item['timestamp']
        action = item['action']
        details = item['details']
        if 'newCharacter' in details:
            new_character = details['newCharacter']
            old_character = None
        if 'oldCharacter' in details:
            old_character = details['oldCharacter']
            new_character = None
        x_coord = details['x']
        y_coord = details['y']
        game_data = (timestamp, action, new_character,old_character, x_coord, y_coord)
        transformed_data.append(game_data)
    return transformed_data

# Exemple d'utilisation
    
gamedata = [{'timestamp': '2024-03-31T04:36:38.721Z', 'action': 'INPUT', 'details': {'newCharacter': 'P', 'x': '4', 'y': '12'}},{'timestamp': '2024-03-31T04:40:53.768Z', 'action': 'CORRECT', 'details': {'newCharacter': 'P', 'x': '4', 'y': '5'}}]
print(gamedata)
transformed_gamedata = transform_data(gamedata)
print(transformed_gamedata)
