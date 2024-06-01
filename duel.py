import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Raw data provided by the user
data = """
2024-03-31T04:36:38.721Z;CELL_INPUT;newCharacter=P,x=4,y=12,
2024-03-31T04:36:38.761Z;CELL_CORRECT;newCharacter=P,x=4,y=12,
2024-03-31T04:36:39.667Z;CELL_INPUT;newCharacter=S,x=5,y=12,
2024-03-31T04:36:39.682Z;CELL_CORRECT;newCharacter=S,x=5,y=12,
2024-03-31T04:37:43.484Z;CELL_INPUT;newCharacter=W,x=11,y=0,
2024-03-31T04:37:43.513Z;CELL_WRONG;newCharacter=W,x=11,y=0,
2024-03-31T04:37:44.437Z;CELL_INPUT;newCharacter=G,x=11,y=1,
2024-03-31T04:37:44.458Z;CELL_WRONG;newCharacter=G,x=11,y=1,
2024-03-31T04:37:44.627Z;CELL_INPUT;newCharacter=E,x=11,y=2,
2024-03-31T04:37:44.644Z;CELL_WRONG;newCharacter=E,x=11,y=2,
2024-03-31T04:37:44.861Z;CELL_INPUT;newCharacter=T,x=11,y=3,
2024-03-31T04:37:44.873Z;CELL_WRONG;newCharacter=T,x=11,y=3,
"""

# Splitting the data into lines
lines = data.strip().split("\n")

# Extracting only the CELL_CORRECT lines
correct_lines = [line for line in lines if "CELL_CORRECT" in line]

# Extracting the maximum x and y values to determine the grid size
max_x = 0
max_y = 0
cells = []

for line in correct_lines:
    match = re.search(r'newCharacter=(\w),x=(\d+),y=(\d+)', line)
    if match:
        char, x, y = match.groups()
        x, y = int(x), int(y)
        cells.append((char, x, y))
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

# Creating the grid
grid = np.full((max_x + 1, max_y + 1), '', dtype=str)

# Filling the grid with the correct characters
for char, x, y in cells:
    grid[x, y] = char

# Displaying the grid as a DataFrame for better readability
grid_df = pd.DataFrame(grid)
grid_df
