# Mars Rover Simulator

Toy robot simulator for a 5x5 tabletop (valid coordinates are from 0 to 4).

## Commands Supported
- PLACE X,Y,FACING
- MOVE
- LEFT
- RIGHT
- REPORT

Valid directions: NORTH, EAST, SOUTH, WEST

---

## Run (Interactive Mode)

- Run the program: 
py rover.py 

- Type commands into the terminal (one per line). Example:

PLACE 0,0,NORTH
MOVE
REPORT

## Run (using a Test Case File)
- Run using a command file:
py rover.py Test_Cases\01_basic_move.txt
- This runs the simulator using command inputs stored inside the Test_Cases/ folder.

## Test Cases 
- A set of .txt test case files are provided in the Test_Cases/ directory.
- Each file contains a sequence of commands to exercise the simulator.


## Optional Plot mode 

To enable the live 2D plot (requires matplotlib):

    py rover.py --plot
    py rover.py Test_Cases\01_basic_move.txt --plot
