# create_Labyrinth.py
#------------------------------------------------------------------------------
import random
from typing import List, Tuple

# Funktion erstellt ein Gitter aus '#' und ' ' 
def create_lattice(
  size: int
) -> Tuple[List]:
    """
    @param size: Seitenlaenge des  Quadrates
    return:
    lattice: Gitter aus '#' und ' '
    """
    # Liste bildet spaeter das Gitter 
    lattice =[]

    # Erzeugen Liste mit '#'-Eintraegen  
    list_cont = ['#']*size

    # for-Schleife fuer alternierend '#' und ' ' Eintraege
    list_alter = []
    for i in range(size):
        if i%2 == 0:  
            list_alter += ['#']
        else:  # falls nicht " " 
            list_alter +=[' ']

    # Zusammenbau Listen zu 2D-Liste 
    for i in range(size):
        # gerade Zahlen liste_cont 
        if i % 2 == 0:
            lattice += [list_cont.copy()]
        # ungerade Zahlen liste_alter 
        else:
            lattice += [list_alter.copy()]

    return(lattice)  # Rueckgabe der 2D-Liste 


# Erzeuge Zufaelliges Labyrinth
def Labyrinth_Rekursion(
  row: int,
  column: int,
  edge_length: int,
  maze: List
):
  """
  @param row: Zeilenidex fuer ersten Mittelpunkt aus Liste
  @param column: Spaltenindex -||-
  @param edge_length: Seitenlaenge des naechstkleineren Quadrats
  @param maze: 2D-Liste (Gitter)
  return:
  maze: zufaelliges Labyrinth 
  """

  # Abbruchbedingung: edge_length kleiner als 2 dann kein Mittelpunkt mehr findbar 
  if edge_length <2:
    return(maze)

  else:
    
    # Entfernen von Haschtags ("Waende")
    maze[row][column + random.randrange(1, edge_length, 2)] = " " # Random herausschlagen unten
    maze[row+random.randrange(1, edge_length, 2)][column] = " "  # -||-  rechts
    maze[row-random.randrange(1, edge_length, 2)][column] = " "  # -||-  links 
    maze[row][column -random.randrange(1, edge_length, 2)] = " " # -||-  oben
    
    # Halbieren der edge_length fuer Berechnung spaetere Mittelpunktsberechnung 
    half_size = edge_length // 2 

    #Funktion neu aufrufen, kleinere Quadrate: 
    Labyrinth_Rekursion(row + half_size, column + half_size, half_size, maze) # unten rechts
    Labyrinth_Rekursion(row + half_size, column - half_size, half_size, maze) # unten links
    Labyrinth_Rekursion(row - half_size, column + half_size, half_size, maze) # oben rechts
    Labyrinth_Rekursion(row - half_size, column - half_size, half_size, maze) # oben links

# Testfunktion
def test():

  # Eingabe durch Benutzer 
  eingabe = input(
  "Geben Sie eine Zahl n ein, mit welcher ein quadratisches \n Labyrinth der Groesse 2**n +1 erzeugt wird: "
  )
  
  size = 2 **int(eingabe) + 1 # Berechne Quadratgroesse 
  labyrinth = create_lattice(size) 
  
  # Berechne ersten Mittelpunkt
  row = size // 2  # Zeilenindex der Liste fuer erst Mittelpunkt 
  column = size// 2  # Spaltenindex der Liste fuer ersten Mittelpunkt
  
  # Funktionsaufruf mit Seiteneffekt 
  Labyrinth_Rekursion(row, column, edge_length = size // 2, maze = labyrinth)

  #Rueckgabewert an die Mainfunktion
  return(labyrinth)  

#------ Main-Funktion -----------------
if __name__ == "__main__":
    test()

