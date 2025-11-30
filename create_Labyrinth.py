# create_Labyrinth.py
#------------------------------------------------------------------------------
import random
from typing import List, Tuple

# Function creates a grid of '#' and ' ' 
def create_lattice(
  size: int
) -> Tuple[List]:
    """
    @param size: Side length of the square
    return:
    lattice: Grid of '#' and ' '
    """
    # List will later form the grid
    lattice =[]

    # Create list with '#' entries  
    list_cont = ['#']*size

    # for-loop for alternating '#' and ' ' entries
    list_alter = []
    for i in range(size):
        if i%2 == 0:  
            list_alter += ['#']
        else:  # otherwise " " 
            list_alter +=[' ']

    # Combine lists into 2D list 
    for i in range(size):
        # even rows list_cont 
        if i % 2 == 0:
            lattice += [list_cont.copy()]
        # odd rows list_alter 
        else:
            lattice += [list_alter.copy()]

    return(lattice)  # Return 2D list 


# Generate random labyrinth
def Labyrinth_Rekursion(
  row: int,
  column: int,
  edge_length: int,
  maze: List
):
  """
  @param row: Row index for first center from list
  @param column: Column index -||-
  @param edge_length: Side length of next smaller square
  @param maze: 2D list (grid)
  return:
  maze: Random labyrinth 
  """

  # Base case: edge_length smaller than 2, no center can be found 
  if edge_length <2:
    return(maze)

  else:
    
    # Remove hashtags ("walls")
    maze[row][column + random.randrange(1, edge_length, 2)] = " " # Random remove down
    maze[row+random.randrange(1, edge_length, 2)][column] = " "  # -||-  right
    maze[row-random.randrange(1, edge_length, 2)][column] = " "  # -||-  left 
    maze[row][column -random.randrange(1, edge_length, 2)] = " " # -||-  up
    
    # Halve edge_length for later center calculation 
    half_size = edge_length // 2 

    # Recursively call function for smaller squares: 
    Labyrinth_Rekursion(row + half_size, column + half_size, half_size, maze) # bottom right
    Labyrinth_Rekursion(row + half_size, column - half_size, half_size, maze) # bottom left
    Labyrinth_Rekursion(row - half_size, column + half_size, half_size, maze) # top right
    Labyrinth_Rekursion(row - half_size, column - half_size, half_size, maze) # top left

# Test function
def test():

  # Input from user 
  eingabe = input(
  "Enter a number n to generate a square \n labyrinth of size 2**n +1: "
  )
  
  size = 2 **int(eingabe) + 1 # Calculate square size 
  labyrinth = create_lattice(size) 
  
  # Calculate first center
  row = size // 2  # Row index of list for first center 
  column = size// 2  # Column index of list for first center
  
  # Function call with side effect 
  Labyrinth_Rekursion(row, column, edge_length = size // 2, maze = labyrinth)

  # Return value to main function
  return(labyrinth)  

#------ Main function -----------------
if __name__ == "__main__":
    test()
