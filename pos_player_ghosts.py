# pos_player_ghosts.py
#------------------------------------------------------------------------------ 
# importiere Module 
import random
import pygame
from typing import List, Tuple

# Konstante Informationen fuer die Funktionen
# Groesse der Pixel der Sprites
CELL_SIZE = 16 

# Funktion Berechnung Starposition der  Geister
def pos_geister(
    number_ghosts: int,
    labyrinth: List,
) -> Tuple[List]:
    """
    @param number_ghots: Anzahl der Geister
    @param labyrinth: generierte Zufallslabyrinth aus create_labyrinth.py generiert in Mainfunction
    return:
    list_ghost: Liste der Geister, enthaelt Starposition, Bewegungsrichtung, Imgae, slowness, counter
    """
  
    # list_ghost ist Liste welche Startpunkte der Geister, sowie deren Startposition enthält 
    list_ghosts =[]
  
    # die 1en und 2en kommen daher, dass das Labyrinth, welches als Liste uebergeben
    # wird, mit Waenden umrandet ist und daher 0,0 und len(labyrinth) einen Baustein zu groß sind
    # Quadratische Labyrinth vier Ecken --> Berechnung der vier Eckkoordinaten
    # multiplizieren mit CELL_SIZE fuer die Startposition in Pixeln
  
    # x, y Koordinaten Ecke oben rechts fuer Startpunkt der Geister
    x_pos_corner1 = (len(labyrinth) - 2) * CELL_SIZE
    y_pos_corner1 = 1 * CELL_SIZE
    # x, y Koordinaten Ecke oben links fuer Startpunkt der Geister
    x_pos_corner2 = 1 * CELL_SIZE
    y_pos_corner2 = 1 * CELL_SIZE
    # x, y Koordinaten Ecke unten rechts fuer Startpunkt der Geister
    x_pos_corner3 = (len(labyrinth) - 2) * CELL_SIZE
    y_pos_corner3 = (len(labyrinth) - 2) * CELL_SIZE
    # x, y Koordinaten Ecke untenlinks fuer Startpunkt der Geister
    x_pos_corner4 = 1 * CELL_SIZE
    y_pos_corner4 = (len(labyrinth) - 2) * CELL_SIZE

    # waehlen einer zufaelligen Startrichtung 
    start_direction = random.choice(["up", "down", "left", "right" ])

    # Liste Namen/Dateipfad der Bilddateien 
    PIC_GHOSTS = ["bilder/ghosts/blinky.png", "bilder/ghosts/clyde.png", "bilder/ghosts/inky.png", "bilder/ghosts/pinky.png"]
    counter = 0 # Counter fuer Verlangsamung --> Anfangs 0 
    slowness = False  # slowness auf False, da noch kein Spieler-Geist-Kontakt vorliegt 

    # while-Schleife --> Verteilung der Geister gleichmaessig auf 4 Ecken bis alle verteilt sind 
    while number_ghosts > 0:

        if number_ghosts != 0:  # Zuweisung Geist Ecke, uebergabe der Koordinaten, Startrichtung, Sprite, slowness und counter 
            list1 = [x_pos_corner1, y_pos_corner1, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter ]
            list_ghosts += [list1.copy()]
            number_ghosts -= 1  # Abziehen von Anzahl nach Zuweisung 
      
        if number_ghosts != 0:  # Zuweisung Geist Ecke, uebergabe der Koordinaten, Startrichtung, Sprite, slowness und counter 
            list2 = [x_pos_corner2, y_pos_corner2, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter]
            list_ghosts += [list2.copy()]
            number_ghosts -= 1
      
        if number_ghosts != 0:  # Zuweisung Geist Ecke, uebergabe der Koordinaten, Startrichtung, Sprite, slowness und counter 
            list3 = [x_pos_corner3, y_pos_corner3, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter ]
            list_ghosts += [list3.copy()]
            number_ghosts -= 1  # Abziehen von Anzahl nach Zuweisung 
      
        if number_ghosts != 0:  # Zuweisung Geist Ecke, uebergabe der Koordinaten, Startrichtung, Sprite, slowness und counter 
            list4 = [x_pos_corner4, y_pos_corner4, random.choice(["up", "down", "left", "right" ]), pygame.image.load(random.choice(PIC_GHOSTS)), slowness, counter ]
            list_ghosts += [list4.copy()]
            number_ghosts -= 1  # Abziehen von Anzahl nach Zuweisung 

    # Rueckgabe der Liste 
    return(list_ghosts)


# Funktion Berechung Startposition Spieler
def pos_player(
  labyrinth: List
) -> Tuple[int, int]:
    """
    @param labyrinth: generierte Zufallslabyrinth aus create_labyrinth.py generiert in Mainfunction
    returns:
    player_pos_x, player_pos_y: Koordinaten des Spielers (Pixel)
    """

    zaehler = 0
    # Bedigung, wenn Feld gefunden: False 
    field_find = True 

    while field_find:

        # Zaehler fuer Erhoehung Position nach "rechts" in Liste 
        zaehler += 1
        # Durchlaufen Zeile nach "rechts" mit Zaehler ausgehend von Mitte des Labyrinths   
        if labyrinth[len(labyrinth)//2][len(labyrinth)//2 + zaehler] == " ": # Freies Feld ' ' gefunden 
            field_find = False  # Bedingung False 

    # Skalieren Position auf Koordinaten auf dem Bildschirm: multiplikation mit cell_size
    player_pos_x = (len(labyrinth)//2 + zaehler) * CELL_SIZE
    player_pos_y = (len(labyrinth)//2) * CELL_SIZE

    # Rueckgabe der Koordinaten  
    return player_pos_x, player_pos_y

    
