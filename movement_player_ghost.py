# movement_player_ghosts.py
#------------------------------------------------------------------------------
import random
import pygame
from typing import List, Tuple

# Constant information for the functions
# Size of the sprite pixels
CELL_SIZE = 16

# Provide queries for the directions 
DIRECTIONS = {
    "up": {1: "up", 2: "right", 3 : "left" },
    "down": {1: "down", 2: "right", 3 : "left" },
    "left": {1: "left", 2: "up", 3 : "down" },
    "right": {1: "right", 2: "up", 3 : "down" },
}

# Define the comparison color Neonblue ("wall") 
NEONBLUE = (25, 25, 166)

# Create lists of images for player animation per direction (3 images each), load the images
player_up = [pygame.image.load(f'bilder/pacman-up/{i}.png') for i in range(1, 4)]
player_down = [pygame.image.load(f'bilder/pacman-down/{i}.png') for i in range(1, 4)]
player_left = [pygame.image.load(f'bilder/pacman-left/{i}.png') for i in range(1, 4)]
player_right = [pygame.image.load(f'bilder/pacman-right/{i}.png') for i in range(1, 4)]

# Function to calculate ghost movement
def calculate_ghost_movement(
    direction_ghost: str, 
    ghost_pos_x: int, 
    ghost_pos_y: int, 
    labyrinth: List, 
    slowness: bool, 
    counter: int
) -> Tuple[str, int, int, bool]:
    """
    @param direction_ghost: Ghost movement direction
    @param ghost_pos_x: Ghost x-coordinate (pixel)
    @param ghost_pos_y: Ghost y-coordinate (pixel)
    @param labyrinth: Generated labyrinth from create_labyrinth
    @param slowness: Bool if powerup is active and contact with player
    @param counter: For halving speed when slowness == True 
    returns:
    direction_ghost: Current ghost direction 
    ghost_pos_x: New ghost x-coordinate
    ghost_pos_y: New ghost y-coordinate
    counter: Counter if slowed 
    """
      
    # Check if ghost position is an integer multiple of CELL_SIZE --> then direction change is possible 
    if ghost_pos_x % CELL_SIZE == 0 and ghost_pos_y % CELL_SIZE == 0:
        list_pos_x = ghost_pos_x // CELL_SIZE
        list_pos_y = ghost_pos_y // CELL_SIZE

        # List of possible directions
        possible_directions = []
    
        # 3 possible directions
        direction1 = True
        direction2 = True
        direction3 = True

        # Check which direction the ghost has chosen
        if direction_ghost == "up":
            
            # Check if directions up, right, left are not walls ("#") and the path is free
            direction1 = (labyrinth[list_pos_y - 1][list_pos_x] != "#") # up
            direction2 = (labyrinth[list_pos_y][list_pos_x + 1] != "#") # right
            direction3 = (labyrinth[list_pos_y][list_pos_x - 1] != "#") # left

            # Change direction if all directions blocked
            if not (direction1 or direction2 or direction3):
                possible_directions += ["down"]
        
        elif direction_ghost == "down":
            
            # Check if directions down, right, left are not walls ("#") and the path is free
            direction1 = (labyrinth[list_pos_y + 1][list_pos_x] != "#") # down
            direction2 = (labyrinth[list_pos_y][list_pos_x + 1] != "#") # right
            direction3 = (labyrinth[list_pos_y][list_pos_x - 1] != "#") # left
            # Change direction if all directions blocked
            if not (direction1 or direction2 or direction3):
                possible_directions += ["up"]
        
        elif direction_ghost == "left":
            
            # Check if directions left, up, down are not walls ("#") and the path is free
            direction1 = (labyrinth[list_pos_y][list_pos_x - 1] != "#") # left
            direction2 = (labyrinth[list_pos_y - 1][list_pos_x] != "#") # up
            direction3 = (labyrinth[list_pos_y + 1][list_pos_x] != "#") # down
            
            # Change direction if all directions blocked
            if not (direction1 or direction2 or direction3):
                possible_directions += ["right"]
        
        elif direction_ghost == "right":
            
            # Check if directions right, up, down are not walls ("#") and the path is free
            direction1 = (labyrinth[list_pos_y][list_pos_x + 1] != "#") # right
            direction2 = (labyrinth[list_pos_y - 1][list_pos_x] != "#") # up
            direction3 = (labyrinth[list_pos_y + 1][list_pos_x] != "#") # down

            # Change direction if all directions blocked
            if not (direction1 or direction2 or direction3):
                possible_directions += ["left"]
        
        # If movement possible --> append to list
        if direction1:
            possible_directions.append(DIRECTIONS[direction_ghost][1])
        if direction2:
            possible_directions.append(DIRECTIONS[direction_ghost][2])
        if direction3:
            possible_directions.append(DIRECTIONS[direction_ghost][3])

        # Random choice if possible 
        direction_ghost = random.choice(possible_directions)

    # If slowness not active --> ghost moves fast
    if not slowness:
        # Calculate new coordinates: move by adding/subtracting +-1 
        if direction_ghost == "up": # up
            ghost_pos_y -= 1

        elif direction_ghost == "down": # down
            ghost_pos_y += 1

        elif direction_ghost == "left": # left
            ghost_pos_x -= 1

        elif direction_ghost == "right": # right
            ghost_pos_x += 1

    # If slowness active --> slower movement
    else:

        # Counter: move every 2nd loop --> slower
        counter += 1
        if counter >=2:
            counter = 0
        
            # Calculate new coordinates: move by adding/subtracting +-1
            if direction_ghost == "up": # up
                ghost_pos_y -= 1

            elif direction_ghost == "down": # down
                ghost_pos_y += 1

            elif direction_ghost == "left": # left
                ghost_pos_x -= 1

            elif direction_ghost == "right": # right
                ghost_pos_x += 1

    # Return variables 
    return direction_ghost, ghost_pos_x, ghost_pos_y, counter



# Function to calculate player movement
def calculate_player_movement(
    screen: pygame.Surface, 
    next_direction: str, 
    direction: str, 
    player_pos_x: int, 
    player_pos_y: int, 
    picture_player: pygame.Surface, 
    player_image_index: int,
):
    """
    @param screen: Contains pixel color values on the screen
    @param next_direction: New direction of the player
    @param direction: Current direction of the player; string
    @param player_pos_x: x-coordinate (pixel)
    @param player_pos_y: y-coordinate (pixel)
    @param picture_player: Player image
    @param player_index: Index for selecting image from list 
    returns:
    next_direction: For new direction 
    direction: Current direction
    player_pos_x: New x-coordinate (pixel)
    player_pos_y: New y-coordinate (pixel)
    picture_player: Loaded image 
    player_image_index: Index for image change
    """                       
      
    # Determine colors around the player to check if path is possible
    color_player_top = screen.get_at((player_pos_x + CELL_SIZE//2 -1 , player_pos_y -1))
    color_player_bottom = screen.get_at((player_pos_x + CELL_SIZE//2 -1 , player_pos_y + CELL_SIZE))
    color_player_left = screen.get_at((player_pos_x -1, player_pos_y + CELL_SIZE//2 -1 ))
    color_player_right = screen.get_at((player_pos_x + CELL_SIZE , player_pos_y + CELL_SIZE//2 -1))

    # Check integer multiples of player position in list
    # Movement on list indices for direction change is mandatory 
    list_pos_x = player_pos_x % CELL_SIZE
    list_pos_y = player_pos_y % CELL_SIZE

    # If no new input, keep old direction until change is possible 
    # Check each time if movement is possible
    # If movement possible, update direction
    if next_direction is not None:
        if next_direction == "up" and color_player_top != NEONBLUE and list_pos_x== 0:
            direction = next_direction
            next_direction = None  # Reset stored direction
        elif next_direction == "down" and color_player_bottom != NEONBLUE and list_pos_x == 0:
            direction = next_direction
            next_direction = None
        elif next_direction == "left" and color_player_left != NEONBLUE and list_pos_y == 0:
            direction = next_direction
            next_direction = None
        elif next_direction == "right" and color_player_right != NEONBLUE and list_pos_y == 0:
            direction = next_direction
            next_direction = None
    
    # Execute movement as long as possible 
    if direction == "up" and color_player_top != NEONBLUE and list_pos_x == 0:
        player_pos_y -= 1  # Move player up
        picture_player = player_up[int(player_image_index)]
    elif direction == "down" and color_player_bottom != NEONBLUE and list_pos_x == 0:
        player_pos_y += 1  # Move player down
        picture_player = player_down[int(player_image_index)]
    elif direction == "left" and color_player_left != NEONBLUE and list_pos_y == 0:
        player_pos_x -= 1  # Move player left
        picture_player = player_left[int(player_image_index)]
    elif direction == "right" and color_player_right != NEONBLUE and list_pos_y== 0:
        player_pos_x += 1  # Move player right
        picture_player = player_right[int(player_image_index)]

    # Return variables 
    return next_direction, direction, player_pos_x, player_pos_y, picture_player, player_image_index
