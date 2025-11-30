# Importiere pygame und random 
import pygame
import random
import time

# Importiere eigens geschriebene Module
import create_Labyrinth  # Modul das das Labyrinth erzeugt 
import movement_player_ghost  # Modul das das Bewegungsmuster des Geistes und des Spielers berechnet
import pos_player_ghosts  # Modul, dass die anfaengliche Positionen der Geister und des Spielers bestimmt 

# Text fuer Sieg oder Niederlage beim Spiel 
def draw_game_over(screen: pygame.Surface, spieltext: str):
    font = pygame.font.Font(None,30)  # Schriftart und Schriftgroesse 
    text = font.render(spieltext, True, (255, 0, 0))  #Textfeld mit Textnamen, Farbe Rot 
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))  # erstelle Rectangle in Zentrum vom Bildschirm 
    screen.blit(text, text_rect) # Darstellung 

if __name__ == "__main__":

    # Initialisierung 
    pygame.init()  # Pygame 
    pygame.mixer.init()  # Mixer von Pygame 

    # Musik
    SOUND_GAMESTART = pygame.mixer.Sound("sounds/game_start.wav")  # Lade fuer Spielstart 
    SOUND_POWERUP = pygame.mixer.Sound("sounds/power_pellet.wav")  # Lade Sound fuer Powerup 
    SOUND_PLAYER_LOST = pygame.mixer.Sound("sounds/death_1.wav")  # Lade Sound fuer Tod vom Spieler
    SOUND_PLAYER = pygame.mixer.Sound("sounds/credit.wav")  # Lade Fresssound 
    player_death_sound_played = False  # Variable, ob der Sound für den Spieler-Tod bereits abgespielt wurde
    player_sound_playing = False  # Variable, ob der Sound bereits abgespielt wurde

    # Soundkanaele
    pygame.mixer.set_num_channels(3) # Anzahl Soundkanaele 3, da 3 gleichzeitig abspielbar
    # Zweiten Sound-Kanal fuer Powerup Sound
    powerup_channel = pygame.mixer.Channel(1)
    # Sound fuer Start des Spiels --> spearater Kanal
    start_sound_channel = pygame.mixer.Channel(2)

    
    # Erzeugung des Labyrinths durch Fkt. in Modul create_Labyrinth
    labyrinth = create_Labyrinth.test()

    # Groeße des Fensters und der Zellen im Labyrinth
    size = len(labyrinth)  # Seitenlaenge size des labyrinths 
    CELL_SIZE = 16  # Groesse der Pixel der Sprites
    window_size = (size * CELL_SIZE, size * CELL_SIZE) # Fenstergoesse fuer das Spiel

    # erstelle Uhr 
    clock = pygame.time.Clock()  

    # Geister
    # Anzahl der Geister als Gegener
    number_ghosts = int(input("Geben Sie die Anzahl der Geister an, gegen die Sie spielen wollen. "))
    # Liste enhaelt berechnete Position und Farbe der Gesiter mit der Funktion pos_geister
    list_ghosts = pos_player_ghosts.pos_geister(number_ghosts, labyrinth) 
    # Index fuer das Wechseln der Farbe der Geister, bei Powerup 
    ghost_image_index = 0
    PICTURE_GHOST_BLUE = pygame.image.load("bilder/ghosts/blue_ghost.png")  # Lade Bild blauen Geist 
    slowness = False # Verlangsamung des Geistes 

    # Spieler  
    player_pos_x, player_pos_y = pos_player_ghosts.pos_player(labyrinth)  # Startpostion des Spielers
    picture_player = pygame.image.load("bilder/pacman-left/1.png")  # Startbild des Spielers
    player_rect = picture_player.get_rect(topleft = (player_pos_x, player_pos_y))  
    player_image_index = 0 # Index fuer Animation 

    # Lade die Bilder fuer die kleinen und großen (Powerup) Punkte 
    PICTURE_DOT_SMA = pygame.image.load("bilder/other/dot.png")  # Lade Bild kleiner Dot
    PICTURE_DOT_BIG = pygame.image.load("bilder/other/big_dot.png")  # Lade Bild Powerup-Dot 

    # Powerup 
    # Definiere Powerup mit bool: falls True gibt unsterblichkeit fuer 8 Sekunden 
    Powerup = False
    POWERUP_DURATION = 8000  # Powerup- Dauer in Milisekunden (8 Sekunden)
    powerup_start_time = 0  # Zeitpunkt, an dem Powerup aktiviert wurde

    # Farben
    BLACK = (0, 0, 0)  # Fuer den Hintergrund 
    NEONBLUE = (25, 25, 166)  # Als Wandfarbe 

    # Erzeugung des Pygame-Fensters
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pycman")  # Spielfenster Titel

    # Hauptprogrammschleife
    running = True  # Dauerschleife 
    moving = False  # Bewegung False, noch keine Spielbewegung 
    direction = None  # keine Anfangsrichtung des Spielers 
    next_direction = None # noch Richtungswechsel des Spielers 
    game_text = None  # Spaeter "Game Over" oder "You won"
    start_sound_channel.play(SOUND_GAMESTART) 
    while running:
    
        # Ueberpuefe die Evente die in Pygame ablaufen 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False  
            
            # Tastatureingaben abfangen um den Spieler zu steuern 
            if event.type == pygame.KEYDOWN:
                moving = True  # Spielstart 
                if event.key == pygame.K_w:
                    next_direction = "up"  # Bewegung nach oben
                elif event.key == pygame.K_s:
                    next_direction = "down"  # Bewegung nach unten
                elif event.key == pygame.K_a:
                    next_direction = "left"  # Bewegung nach links
                elif event.key == pygame.K_d:
                    next_direction = "right" # Bewegung nach rechts
                
        # Tastatureingabe erfolgte: Spielstart durch Bewegung
        if moving:

            # wenn der Spielersound noch nicht gespielt: unendlosschleife gestartet
            if not player_sound_playing:
                SOUND_PLAYER.play(-1)  # -1 = Endlosschleife
                player_sound_playing = True  # Sound abgespielt 
      
            # Spieler Animation und Bewegung 
            player_image_index +=0.3 # durchlaufen des Index fuer Animation
            # 3 Bilder, sobald 3 erreicht Zuruecksetzung Index
            if player_image_index >3: 
                player_image_index =0  

            # Berechnung Bewegungsrichtung Spieler
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

            # Geist Bewegung und Animation  
            # Durchlaufen der Liste mit Anzahl i Geister 
            for i in range(len(list_ghosts)):

                # Berechne Position des Geistes
                # und ueberschreibe die neue Position auf die alte
                direction_geist, ghost_pos_x, ghost_pos_y , counter = movement_player_ghost.calculate_ghost_movement(
                    list_ghosts[i][2], # direction_ghost
                    list_ghosts[i][0], # ghost_pos_x
                    list_ghosts[i][1], # ghost_pos_y
                    labyrinth, # labyrinth
                    list_ghosts[i][4], # slowness
                    list_ghosts[i][5]  # counter 
                )
                # ueberschreiben der neu berechneten Parameter
                list_ghosts[i][2] = direction_geist
                list_ghosts[i][0] = ghost_pos_x # x- Koordinate 
                list_ghosts[i][1] = ghost_pos_y # y- Koordinate 
                list_ghosts[i][5] = counter # counter falls Spieler-Geist-Kontakt
        
        # fuelle den Hintergrund schwarz auf der Ebene screen 
        screen.fill(BLACK)
    
        # male auf den schwarzen Hintergrund Labyrinth (2D-Liste) 
        for i in range(size):  # Auswal der Zeile 
            for j in range(size):  # Auswahl der Spalte 
                x = j * CELL_SIZE # skaliere die Liste mit CELL_SIZE
                y = i * CELL_SIZE # -||-
                    
                # Male Waende
                # ueberall wo '#' male ein neonblaues Quadrat
                if labyrinth[i][j] == '#':
                    # groesse CELL_SIZE an der Position x und y 
                    pygame.draw.rect(screen, NEONBLUE, (x, y, CELL_SIZE, CELL_SIZE))  

                # Male Dots  
                if labyrinth[i][j] == ' ':

                    # Male Big Dot
                    # Powerup, wenn Position i, j von '## umgeben ist 
                    if labyrinth[i + 1][j] == labyrinth [i][j + 1] == '#':
                        # Rectangle aus Big-Dot Sprite (Grund: Kollisionserkennung mit Spieler spaeter) 
                        big_dot_rect = PICTURE_DOT_BIG.get_rect(topleft = (j*CELL_SIZE, i*CELL_SIZE))  
                        # male grossen Dot 
                        screen.blit(PICTURE_DOT_BIG, (j*CELL_SIZE, i*CELL_SIZE))  

                        # Spielerkollision mit Mittelpunkt von Big-Dot
                        # ganzzahliges vielfaches von der Spielerposition
                        # Powerupzeit aktiv 
                        if (
                            player_rect.collidepoint(big_dot_rect.center) and
                            player_pos_x % CELL_SIZE == 0 and
                            player_pos_y % CELL_SIZE == 0
                            ):
                            Powerup = True  
                            # Startzeit für 8 Sec Powerup-Zeit 
                            powerup_start_time = pygame.time.get_ticks() 
                            
                    # Male kleinen Dot 
                    else:
                        # Wo kein grosser Punkt --> wird kleiner Punkt gemalt
                        screen.blit(PICTURE_DOT_SMA, (j*CELL_SIZE, i*CELL_SIZE))   

                # Entferne Dot
                # wo Spieler drüber Dots verschwinden: ersetzen von " " durch "1" in labyrinth
                # da sonst nur Abfrage nach ' ', '#': 1en ist beschrittener Weg  
                if i == (player_pos_y // CELL_SIZE ) and j == (player_pos_x // CELL_SIZE ):                         
                    labyrinth[i][j] = "1"
                
        # Powerup beruehrt/ gefressen? 
        if Powerup:
            # Berechne Powerupzeit 
            current_time = pygame.time.get_ticks()  # aktuelle Spielzeit 
            elapsed_time = current_time - powerup_start_time  # Vergangene Spielzeit 

            # wenn die vergangene Zeit groesser als 8 sec, dann Powerupzeit vorbei
            if elapsed_time >= POWERUP_DURATION:
                Powerup = False 
                slowness = False # slowness fuer Geister 
                powerup_channel.stop()  # Powerup-Sound stoppen
            else:
                # Powerup-Sound nur abspielen, wenn er noch nicht abgelaufen ist
                if not powerup_channel.get_busy():
                    powerup_channel.play(SOUND_POWERUP)  # Einmalig abspielen

        # Abfrage ob ein Leerstring in Liste vorkommt: nein --> Spieler gewonnen                   
        if ' ' not in [item for sublist in labyrinth for item in sublist]:
            moving = False  # Bewegung Stillstand
            game_text = 'You won'
            draw_game_over(screen, game_text) # game_text Zeichnen 
            SOUND_PLAYER.stop() # SOUND_PLAYER beenden, wenn Spiel beendet wird
            powerup_channel.stop() # Powerup-Sound stoppen
            running = False # Spielabbruch 
            pygame.display.update()
            time.sleep(1)
            
        # Spieler zeichnen
        # Rectangle fuer Kollisionserkennung
        player_rect = picture_player.get_rect(topleft = (player_pos_x, player_pos_y))  
        screen.blit(picture_player,(player_rect))  # Darstellung auf Rectangle screen 

        # Geister zeichnen
        for i in range(len(list_ghosts)):  # Durchlaufe list_ghosts --> jeder Geist gezeichnet 

            #  Powerupzeit nicht aktiv
            if Powerup == False:
                # Rectangle fuer Kollsionserkennung 
                ghost_rect = list_ghosts[i][3].get_rect( topleft= (list_ghosts[i][0], list_ghosts[i][1]))  
                screen.blit(list_ghosts[i][3], ghost_rect)  # Darstellung Geist auf screen 
                
            # Falls ja aendern der Farbe 
            else:
                ghost_slowness = [PICTURE_GHOST_BLUE, list_ghosts[i][3]] #  Liste aus 2 Farben: Geistfarbe und blauen Farbe 
                ghost_image_index +=0.01 # Index fuer Wechsel des Incex in liste ghost_slowness  
                if ghost_image_index >2: 
                    ghost_image_index =0  # Wenn Index groesser als 2 reset auf 0, fuer erneuten Beginn des Farbwechsels, 2 verschiedene Sprites 
                ghost_rect = ghost_slowness[int(ghost_image_index)].get_rect( topleft= (list_ghosts[i][0], list_ghosts[i][1]))  # Auswahl des Sprites
                screen.blit(ghost_slowness[int(ghost_image_index)],ghost_rect)  # Darstellung Geist auf screen 
                
            # Kollision von Geist und Spieler?
            # Kollsion stattgefunden Powerup nicht aktiv
            if player_rect.colliderect(ghost_rect) and Powerup == False:   
                moving = False  # Spielstop 
                game_text = "Game Over"  
                draw_game_over(screen, game_text)# Rufe die Funktion auf, um den game-text zu zeichnen
                
                # Ueberpruefe Geist-Tod-Sound bereits abgespielt?
                if not player_death_sound_played:
                    SOUND_PLAYER.stop() # SOUND_PLAYER beenden 
                    SOUND_PLAYER_LOST.play()  # Geist-Tod-Sound abspielen
                    player_death_sound_played = True  # Sound wurde einmal abgespielt 
                    running = False # Spielabbruch 
                    pygame.display.update()
                    time.sleep(1)
                    
            # Kollision von Geist und Spieler, Powerup nicht aktiv 
            elif player_rect.colliderect(ghost_rect) and Powerup:
                slowness = True  # Verlangsamung aktiv 
                list_ghosts[i][4] = slowness # beruerter Geist verlangsamt 
                
            elif Powerup == False:
                list_ghosts[i][4] = slowness # Verlangsamung zuruekgesetzt

        pygame.display.update()
        # Update des Displays mit 60 FPS
        clock.tick(60)

    # Beenden von Pygame
    pygame.quit()

