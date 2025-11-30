# Import pygame and random 
import pygame
import random
import time

# Import custom modules
import create_Labyrinth  # Module that generates the labyrinth
import movement_player_ghost  # Module that calculates the movement pattern of the ghost and player
import pos_player_ghosts  # Module that determines the initial positions of ghosts and player

# Text for victory or defeat in the game
def draw_game_over(screen: pygame.Surface, spieltext: str):
    font = pygame.font.Font(None,30)  # Font and font size
    text = font.render(spieltext, True, (255, 0, 0))  # Text field with text, color red
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))  # Create rectangle in the center of the screen
    screen.blit(text, text_rect) # Display

if __name__ == "__main__":

    # Initialization
    pygame.init()  # Pygame
    pygame.mixer.init()  # Pygame mixer

    # Music
    SOUND_GAMESTART = pygame.mixer.Sound("sounds/game_start.wav")  # Load sound for game start
    SOUND_POWERUP = pygame.mixer.Sound("sounds/power_pellet.wav")  # Load sound for powerup
    SOUND_PLAYER_LOST = pygame.mixer.Sound("sounds/death_1.wav")  # Load sound for player death
    SOUND_PLAYER = pygame.mixer.Sound("sounds/credit.wav")  # Eating sound
    player_death_sound_played = False  # Variable whether the player death sound has already been played
    player_sound_playing = False  # Variable whether the sound has already been played

    # Sound channels
    pygame.mixer.set_num_channels(3) # Number of sound channels 3, since 3 can play simultaneously
    # Second sound channel for powerup sound
    powerup_channel = pygame.mixer.Channel(1)
    # Sound for game start --> separate channel
    start_sound_channel = pygame.mixer.Channel(2)


    # Generate the labyrinth using function in module create_Labyrinth
    labyrinth = create_Labyrinth.test()

    # Size of the window and cells in the labyrinth
    size = len(labyrinth)  # Side length of the labyrinth
    CELL_SIZE = 16  # Size of the sprite pixels
    window_size = (size * CELL_SIZE, size * CELL_SIZE) # Window size for the game

    # Create clock
    clock = pygame.time.Clock()  

    # Ghosts
    # Number of ghosts as enemies
    number_ghosts = int(input("Enter the number of ghosts you want to play against. "))
    # List contains calculated position and color of ghosts using function pos_geister
    list_ghosts = pos_player_ghosts.pos_geister(number_ghosts, labyrinth)
    # Index for changing ghost color during powerup
    ghost_image_index = 0
    PICTURE_GHOST_BLUE = pygame.image.load("bilder/ghosts/blue_ghost.png")  # Load blue ghost image
    slowness = False # Ghost slowdown

    # Player  
    player_pos_x, player_pos_y = pos_player_ghosts.pos_player(labyrinth)  # Player start position
    picture_player = pygame.image.load("bilder/pacman-left/1.png")  # Player start image
    player_rect = picture_player.get_rect(topleft = (player_pos_x, player_pos_y))  
    player_image_index = 0 # Index for animation

    # Load images for small and big (powerup) dots
    PICTURE_DOT_SMA = pygame.image.load("bilder/other/dot.png")  # Load small dot image
    PICTURE_DOT_BIG = pygame.image.load("bilder/other/big_dot.png")  # Load powerup dot image

    # Powerup
    # Define powerup with bool: if True gives invincibility for 8 seconds
    Powerup = False
    POWERUP_DURATION = 8000  # Powerup duration in milliseconds (8 seconds)
    powerup_start_time = 0  # Time when powerup was activated

    # Colors
    BLACK = (0, 0, 0)  # For the background
    NEONBLUE = (25, 25, 166)  # Wall color

    # Create the Pygame window
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pycman")  # Window title

    # Main program loop
    running = True  # Loop
    moving = False  # Movement False, no game movement yet
    direction = None  # No initial player direction
    next_direction = None # No direction change yet
    game_text = None  # Later "Game Over" or "You won"
    start_sound_channel.play(SOUND_GAMESTART) 
    while running:

        # Check events in Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False  
            
            # Capture key input to control player
            if event.type == pygame.KEYDOWN:
                moving = True  # Game start
                if event.key == pygame.K_w:
                    next_direction = "up"  # Move up
                elif event.key == pygame.K_s:
                    next_direction = "down"  # Move down
                elif event.key == pygame.K_a:
                    next_direction = "left"  # Move left
                elif event.key == pygame.K_d:
                    next_direction = "right" # Move right

        # Key input occurred: game start through movement
        if moving:

            # if player sound not played yet: start endless loop
            if not player_sound_playing:
                SOUND_PLAYER.play(-1)  # -1 = loop
                player_sound_playing = True  # Sound played

            # Player animation and movement
            player_image_index +=0.3 # advance the index for animation
            # 3 images, reset index when 3 reached
            if player_image_index >3: 
                player_image_index =0  

            # Calculate player movement direction
            (
                next_dirction, 
                direction, 
                player_pos_x, 
                player_pos_y, 
                picture_player, 
                player_image_index
            ) = movement_player_ghost.calculate_player_movement(
                screen, 
                next_direction, 
                direction, 
                player_pos_x, 
                player_pos_y, 
                picture_player, 
                player_image_index
            )

            # Ghost movement and animation  
            # Loop through the list with number of ghosts
            for i in range(len(list_ghosts)):

                # Calculate ghost position
                # and overwrite new position over old
                direction_geist, ghost_pos_x, ghost_pos_y , counter = movement_player_ghost.calculate_ghost_movement(
                    list_ghosts[i][2], # direction_ghost
                    list_ghosts[i][0], # ghost_pos_x
                    list_ghosts[i][1], # ghost_pos_y
                    labyrinth, # labyrinth
                    list_ghosts[i][4], # slowness
                    list_ghosts[i][5]  # counter 
                )
                # overwrite the newly calculated parameters
                list_ghosts[i][2] = direction_geist
                list_ghosts[i][0] = ghost_pos_x # x coordinate
                list_ghosts[i][1] = ghost_pos_y # y coordinate
                list_ghosts[i][5] = counter # counter in case of player-ghost contact

        # Fill background black on screen
        screen.fill(BLACK)

        # Draw the labyrinth (2D list) on the black background
        for i in range(size):  # Select row
            for j in range(size):  # Select column
                x = j * CELL_SIZE # scale list with CELL_SIZE
                y = i * CELL_SIZE # -||-

                # Draw walls
                # wherever '#' draw a neon blue square
                if labyrinth[i][j] == '#':
                    # size CELL_SIZE at position x and y
                    pygame.draw.rect(screen, NEONBLUE, (x, y, CELL_SIZE, CELL_SIZE))  

                # Draw dots  
                if labyrinth[i][j] == ' ':

                    # Draw big dot
                    # Powerup, if position i, j is surrounded by '##'
                    if labyrinth[i + 1][j] == labyrinth [i][j + 1] == '#':
                        # Rectangle from Big-Dot sprite (reason: collision detection with player later) 
                        big_dot_rect = PICTURE_DOT_BIG.get_rect(topleft = (j*CELL_SIZE, i*CELL_SIZE))  
                        # draw big dot
                        screen.blit(PICTURE_DOT_BIG, (j*CELL_SIZE, i*CELL_SIZE))  

                        # Player collision with center of big dot
                        # integer multiple of player position
                        # Powerup time active 
                        if (
                            player_rect.collidepoint(big_dot_rect.center) and
                            player_pos_x % CELL_SIZE == 0 and
                            player_pos_y % CELL_SIZE == 0
                            ):
                            Powerup = True  
                            # Start time for 8 sec powerup time 
                            powerup_start_time = pygame.time.get_ticks() 

                    # Draw small dot 
                    else:
                        # Where no big dot --> draw small dot
                        screen.blit(PICTURE_DOT_SMA, (j*CELL_SIZE, i*CELL_SIZE))   

                # Remove dot
                # where player passes over, dots disappear: replace " " with "1" in labyrinth
                # otherwise only check for ' ', '#': 1 is walked path  
                if i == (player_pos_y // CELL_SIZE ) and j == (player_pos_x // CELL_SIZE ):                         
                    labyrinth[i][j] = "1"

        # Powerup touched/eaten? 
        if Powerup:
            # Calculate powerup time 
            current_time = pygame.time.get_ticks()  # current game time 
            elapsed_time = current_time - powerup_start_time  # elapsed game time 

            # if elapsed time greater than 8 sec, powerup time over
            if elapsed_time >= POWERUP_DURATION:
                Powerup = False 
                slowness = False # slowness for ghosts 
                powerup_channel.stop()  # stop powerup sound
            else:
                # Play powerup sound only if it is not already playing
                if not powerup_channel.get_busy():
                    powerup_channel.play(SOUND_POWERUP)  # Play once

        # Check if a space character is in the list: no --> player won                    
        if ' ' not in [item for sublist in labyrinth for item in sublist]:
            moving = False  # Stop movement
            game_text = 'You won'
            draw_game_over(screen, game_text) # Draw game text
            SOUND_PLAYER.stop() # Stop SOUND_PLAYER when game ends
            powerup_channel.stop() # Stop powerup sound
            running = False # Exit game 
            pygame.display.update()
            time.sleep(1)

        # Draw player
        # Rectangle for collision detection
        player_rect = picture_player.get_rect(topleft = (player_pos_x, player_pos_y))  
        screen.blit(picture_player,(player_rect))  # Display on screen

        # Draw ghosts
        for i in range(len(list_ghosts)):  # Loop through list_ghosts --> draw each ghost

            # Powerup time not active
            if Powerup == False:
                # Rectangle for collision detection 
                ghost_rect = list_ghosts[i][3].get_rect( topleft= (list_ghosts[i][0], list_ghosts[i][1]))  
                screen.blit(list_ghosts[i][3], ghost_rect)  # Display ghost on screen 

            # If yes change color
            else:
                ghost_slowness = [PICTURE_GHOST_BLUE, list_ghosts[i][3]] # List of 2 colors: ghost color and blue color 
                ghost_image_index +=0.01 # Index for switching in list ghost_slowness  
                if ghost_image_index >2: 
                    ghost_image_index =0  # Reset index if greater than 2, for new color switch cycle
                ghost_rect = ghost_slowness[int(ghost_image_index)].get_rect( topleft= (list_ghosts[i][0], list_ghosts[i][1]))  # Select sprite
                screen.blit(ghost_slowness[int(ghost_image_index)],ghost_rect)  # Display ghost on screen

            # Collision of ghost and player?
            # Collision occurred, powerup not active
            if player_rect.colliderect(ghost_rect) and Powerup == False:   
                moving = False  # Stop game
                game_text = "Game Over"  
                draw_game_over(screen, game_text)# Call function to draw game text

                # Check if ghost-death sound already played?
                if not player_death_sound_played:
                    SOUND_PLAYER.stop() # Stop SOUND_PLAYER 
                    SOUND_PLAYER_LOST.play()  # Play ghost-death sound
                    player_death_sound_played = True  # Sound played once 
                    running = False # Exit game 
                    pygame.display.update()
                    time.sleep(1)

            # Collision of ghost and player, powerup active 
            elif player_rect.colliderect(ghost_rect) and Powerup:
                slowness = True  # Slowdown active 
                list_ghosts[i][4] = slowness # touched ghost slowed 

            elif Powerup == False:
                list_ghosts[i][4] = slowness # Reset slowdown

        pygame.display.update()
        # Update display at 60 FPS
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
