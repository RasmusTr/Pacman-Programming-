# movement_player_ghosts.py
#------------------------------------------------------------------------------
import random
import pygame
from typing import List, Tuple

# Konstante Informationen fuer die Funktionen
# Groesse der Pixel der Sprites
CELL_SIZE = 16

# Gebe Abfragen die Richtungen 
DIRECTIONS = {
    "up": {1: "up", 2: "right", 3 : "left" },
    "down": {1: "down", 2: "right", 3 : "left" },
    "left": {1: "left", 2: "up", 3 : "down" },
    "right": {1: "right", 2: "up", 3 : "down" },
}

# Definiere die Vergleichsfarbe Neonblue ("Wand") 
NEONBLUE = (25, 25, 166)

# Erstelle Listen mit Bildern, fuer die Animation des Spielers pro Richtung 3 Bilder, Laden der Bilder 
player_up = [pygame.image.load(f'bilder/pacman-up/{i}.png') for i in range(1, 4)]
player_down = [pygame.image.load(f'bilder/pacman-down/{i}.png') for i in range(1, 4)]
player_left = [pygame.image.load(f'bilder/pacman-left/{i}.png') for i in range(1, 4)]
player_right = [pygame.image.load(f'bilder/pacman-right/{i}.png') for i in range(1, 4)]

# Funktion Berechnung der Bewegung des Geistes
def calculate_ghost_movement(
    direction_ghost: str, 
    ghost_pos_x: int, 
    ghost_pos_y: int, 
    labyrinth: List, 
    slowness: bool, 
    counter: int
) -> Tuple[str, int, int, bool]:
    """
    @param direction_ghost: Bewegungsrichtug des Geistes
    @param ghost_pos_x: Koordinate des Geistes in y (Pixel)
    @param ghost_pos_y: Koordinate des Geistes in y (Pixel)
    @param labyrinth: erzeugte Labyrinth aus create_labyrinth
    @param slowness: Bool falls Powerup aktiv und Kontakt mit Spieler
    @param counter: fuer halbierung der Geschwidigkeit bei slowness == True 
    returns:
    direction_ghost: aktuelle Richtung des Geistes 
    ghost_pos_x: neue x-Koordinate des Geistes 
    ghost_pos_y: neue y-Koordinate
    counter: counter falls Verlangsamung 
    """
      
    # Ueberpruefen, ob die Position der Geistfigur bei x_coordinate und y_coordinate dem ganzzahligen Vielfachen
    # von CELL_SIZE entspricht --> dann Richtungswechsel moeglich 
    if ghost_pos_x % CELL_SIZE == 0 and ghost_pos_y % CELL_SIZE == 0:
        list_pos_x = ghost_pos_x // CELL_SIZE
        list_pos_y = ghost_pos_y // CELL_SIZE

        # Liste für die moeglichen Richtungen
        possible_directions = []
    
        # 3 Moegliche Richtungen
        direction1 = True
        direction2 = True
        direction3 = True

        # Ueberpruefe, welche Richtung der Geist gewählt hat
        if direction_ghost == "up":
            
            # Ueberpruefe, ob Richtungen oben, rechts, links keine Wand ("#") sind und somit der Weg frei ist
            direction1 = (labyrinth[list_pos_y - 1][list_pos_x] != "#") # oben
            direction2 = (labyrinth[list_pos_y][list_pos_x + 1] != "#") # rechts
            direction3 = (labyrinth[list_pos_y][list_pos_x - 1] != "#") # links

            # Richtungswechsel, wenn alle Richtungen blockiert sind
            if not (direction1 or direction2 or direction3):
                possible_directions += ["down"]
        
        elif direction_ghost == "down":
            
            # Ueberpruefe, ob Richtungen unten, rechts, links keine Wand ("#") sind und somit der Weg frei ist
            direction1 = (labyrinth[list_pos_y + 1][list_pos_x] != "#") # unten
            direction2 = (labyrinth[list_pos_y][list_pos_x + 1] != "#") # rechts
            direction3 = (labyrinth[list_pos_y][list_pos_x - 1] != "#") # links
            # Richtungswechsel, wenn alle Richtungen blockiert sind
            if not (direction1 or direction2 or direction3):
                possible_directions += ["up"]
        
        elif direction_ghost == "left":
            
            # Ueberpruefe, ob Richtungen unten, rechts, links keine Wand ("#") sind und somit der Weg frei ist
            direction1 = (labyrinth[list_pos_y][list_pos_x - 1] != "#") # links
            direction2 = (labyrinth[list_pos_y - 1][list_pos_x] != "#") # oben
            direction3 = (labyrinth[list_pos_y + 1][list_pos_x] != "#") # unten
            
            # Richtungswechsel, wenn alle Richtungen blockiert sind
            if not (direction1 or direction2 or direction3):
                possible_directions += ["right"]
        
        elif direction_ghost == "right":
            
            # Ueberpruefe, ob Richtungen unten, rechts, links keine Wand ("#") sind und somit der Weg frei ist
            direction1 = (labyrinth[list_pos_y][list_pos_x + 1] != "#") # rechts
            direction2= (labyrinth[list_pos_y - 1][list_pos_x] != "#") # oben
            direction3 = (labyrinth[list_pos_y + 1][list_pos_x] != "#") # unten

            # Richtungswechsel, wenn alle Richtungen blockiert sind
            if not (direction1 or direction2 or direction3):
                possible_directions += ["left"]
        
        # Falls Bewegung moeglich --> Anhaengen an Liste 
        if direction1:
            possible_directions.append(DIRECTIONS[direction_ghost][1])
        if direction2:
            possible_directions.append(DIRECTIONS[direction_ghost][2])
        if direction3:
            possible_directions.append(DIRECTIONS[direction_ghost][3])

        # Zufaellige Auswahl, falls moeglich 
        direction_ghost = random.choice(possible_directions)

    # Verlangsamung nicht aktiv --> Bewegung Geist schnell 
    if not slowness:
        # Die neuen Koordinaten berechnen: ausfuehren der Bewegung durch Addition bzw. subtraktion +-1 
        if direction_ghost == "up": # oben
            ghost_pos_y -= 1

        elif direction_ghost == "down": # unten
            ghost_pos_y += 1

        elif direction_ghost == "left": # links
            ghost_pos_x -= 1

        elif direction_ghost == "right": # rechts
            ghost_pos_x += 1

    # Wenn slowness aktiv Bewegung langsamer 
    else:

        # Counter: dass jeden 2. Durchlauf sich der Geist nach vorne bewegt --> langsamer
        counter += 1
        if counter >=2:
            counter = 0
        
            # Die neuen Koordinaten berechnen: ausfuehren der Bewegung durch Addition bzw. subtraktion +-1
            if direction_ghost == "up": # oben
                ghost_pos_y -= 1

            elif direction_ghost == "down": # unten
                ghost_pos_y += 1

            elif direction_ghost == "left": # links
                ghost_pos_x -= 1

            elif direction_ghost == "right": # rechts
                ghost_pos_x += 1

    # Rueckgabe der Variablen 
    return direction_ghost, ghost_pos_x, ghost_pos_y, counter



# Funktion Berechnung der Bewegung des Spielers
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
    @param screen: Enthaelt Farbwerte der Pixel auf dem Bildschrim
    @param next_direction: neue Richtung des Geistes
    @param direction: aktuelle Richtung des Spielers; Datentyp string
    @param player_pos_x: Koordinate in x (Pixel)
    @param player_pos_y: Koordinate in x (Pixel)
    @param picture_player: Image von dem Spieler
    @param player_index: Index fuer Auswaehlen des Bildes aus Liste 
    returns:
    next_direction: Fuer neue Richtung 
    direction: aktuelle Richtung
    player_pos_x: neu berechnete x-Koordinate (Pixel)
    player_pos_y: neu berechnete x-Koordinate (Pixel)
    picture_player: geladendes Bild 
    player_image_index: Index fuer Bildwechsel
    """                       
                              
    # Bestimme Farben jeweils um den Spieler fuer Moeglichkeit Weg zu beschreiten
    color_player_top = screen.get_at((player_pos_x + CELL_SIZE//2 -1 , player_pos_y -1))
    color_player_bottom = screen.get_at((player_pos_x + CELL_SIZE//2 -1 , player_pos_y + CELL_SIZE))
    color_player_left = screen.get_at((player_pos_x -1, player_pos_y + CELL_SIZE//2 -1 ))
    color_player_right = screen.get_at((player_pos_x + CELL_SIZE , player_pos_y + CELL_SIZE//2 -1))

    # Abfrage ganzzahliges vielfaches von der Position des Spielers in der Liste
    # Bewegung auf List-Indices fuer Richtungswechsel zwingend notwendig 
    list_pos_x = player_pos_x % CELL_SIZE
    list_pos_y = player_pos_y % CELL_SIZE

    # wenn keine neue Eingabe, behalte alte Richtung bei, bis Richtungswechsel moeglich 
    # jedes mal abgefragt ob die Bewegung ueberhaupt moeglich ist
    # wenn Bewegung moeglich wird neue richtung an alte uebergeben
    if next_direction is not None:
        if next_direction == "up" and color_player_top != NEONBLUE and list_pos_x== 0:
            direction = next_direction
            next_direction = None  # Setze die gespeicherte Richtung zurueck
        elif next_direction == "down" and color_player_bottom != NEONBLUE and list_pos_x == 0:
            direction = next_direction
            next_direction = None  # Setze die gespeicherte Richtung zurueck
        elif next_direction == "left" and color_player_left != NEONBLUE and list_pos_y == 0:
            direction = next_direction
            next_direction = None  # Setze die gespeicherte Richtung zurueck
        elif next_direction == "right" and color_player_right != NEONBLUE and list_pos_y == 0:
            direction = next_direction
            next_direction = None  # Setze die gespeicherte Richtung zurueck
    
    # Ausfuehren der Bewegung solange wie moeglich 
    if direction == "up" and color_player_top != NEONBLUE and list_pos_x == 0:
        player_pos_y -= 1  # Spieler nach oben bewegen
        picture_player = player_up[int(player_image_index)]
    elif direction == "down" and color_player_bottom != NEONBLUE and list_pos_x == 0:
        player_pos_y += 1  # Spieler nach unten bewegen
        picture_player = player_down[int(player_image_index)]
    elif direction == "left" and color_player_left != NEONBLUE and list_pos_y == 0:
        player_pos_x -= 1  # Spieler nach links bewegen
        picture_player = player_left[int(player_image_index)]
    elif direction == "right" and color_player_right != NEONBLUE and list_pos_y== 0:
        player_pos_x += 1  # Spieler nach rechts bewegen
        picture_player = player_right[int(player_image_index)]

    # Rueckgabe der Variabelen 
    return next_direction, direction, player_pos_x, player_pos_y, picture_player, player_image_index
