# pos_player_ghosts.py
#------------------------------------------------------------------------------ 
# import modules 
import random
import pygame
from typing import List, Tuple

# Constant information for the functions
# Size of the sprite pixels
CELL_SIZE = 16 

# Function to calculate the starting position of ghosts
def pos_geister(
    number_ghosts: int,
    labyrinth: List,
) -> Tuple[List]:
    """
    @param number_ghosts: Number of ghosts
    @param labyrinth: Generated random labyrinth from create_labyrinth.py in main function
    return:
    list_ghost: List of ghosts containing start position, movement direction, image, slowness, counter
    """
  
    # list_ghosts is the list containing ghost start points and their start position 
    list_ghosts =[]
  
    # The 1s and 2s are because the labyrinth, passed as a list, is bordered with walls 
    # so 0,0 and len(labyrinth) are one unit too large
    # Square labyrinth corners --> calculate four corner coordinates
    # Multiply by CELL_SIZE for start position in pixels
  
    # x, y coordinates top-right corner for ghost start
    x_pos_corner1 = (len(labyrinth) - 2) * CELL_SIZE
    y_pos_corner1 = 1 * CELL_SIZE
    # x, y coordinates top-left corner for ghost start
    x_pos_corner2 = 1 * CELL_SIZE
    y_pos_corner2 = 1 * CELL_SIZE
    # x, y coordinates bottom-right corner for ghost start
    x_pos_corner3 = (len(labyrinth) - 2) * CELL_SIZE
    y_pos_corner3 = (len(labyrinth) - 2) * CELL_SIZE
    # x, y coordinates bottom-left corner for ghost start
    x_pos_corner4 = 1 * CELL_SIZE
    y_pos_corner4 = (len(labyrinth) - 2) * CELL_SIZE

    # choose a random starting direction 
    start_direction = random.choice(["up", "down", "left", "right" ])

    # List of ghost image file paths
    PIC_GHOSTS = ["bilder/ghosts/blinky.png", "bilder/ghosts/clyde.png", "bilder/ghosts/inky.png", "bilder/ghosts/pinky.png"]
    counter = 0 # Counter for slowness --> initially 0 
    slowness = False  # Slowness set to False, no player-ghost contact yet 

    # while loop --> evenly distribute ghosts across 4 corners until all assigned
    while number_ghosts > 0:

        if number_ghosts != 0:  # Assign ghost to corner, pass coordinates, start direction, sprite, slowness, counter 
            list1 = [x_pos_corner1, y_pos_corner1, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter ]
            list_ghosts += [list1.copy()]
            number_ghosts -= 1  # Decrease number after assignment 
      
        if number_ghosts != 0:
            list2 = [x_pos_corner2, y_pos_corner2, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter]
            list_ghosts += [list2.copy()]
            number_ghosts -= 1
          
        if number_ghosts != 0:
            list3 = [x_pos_corner3, y_pos_corner3, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter ]
            list_ghosts += [list3.copy()]
            number_ghosts -= 1
          
        if number_ghosts != 0:
            list4 = [x_pos_corner4, y_pos_corner4, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter ]
            list_ghosts += [list4.copy()]
            number_ghosts -= 1

    # Return the list 
    return(list_ghosts)


# Function to calculate player starting position
def pos_player(
  labyrinth: List
) -> Tuple[int, int]:
    """
    @param labyrinth: Generated random labyrinth from create_labyrinth.py in main function
    returns:
    player_pos_x, player_pos_y: Player coordinates (pixels)
    """

    counter = 0
    # Condition, when field found: False 
    field_find = True 

    while field_find:

        # Counter to increase position to the "right" in the list 
        counter += 1
        # Traverse row to the right from labyrinth center
        if labyrinth[len(labyrinth)//2][len(labyrinth)//2 + counter] == " ": # Free field ' ' found 
            field_find = False  # Condition False 

    # Scale position to screen coordinates: multiply by CELL_SIZE
    player_pos_x = (len(labyrinth)//2 + counter) * CELL_SIZE
    player_pos_y = (len(labyrinth)//2) * CELL_SIZE

    # Return coordinates  
    return player_pos_x, player_pos_y
