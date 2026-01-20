# Test data 


Each file contains a sequence of commands to exercise the toy robot simulator.

## Files, description and expected output 

# Basic test inputs given in the Assignment
01_basic_move.txt -> 
- Tests basic Place+move+Report 
- Expected : Report :- 0,1, North


02_Left_Turn.txt -> 
- Tests left rotation without movement
- Expected : Report:- 3,3,North


03_Sample_Sequence.txt -> 
- Sample sequence from the task PDF  
- Expected : Report:- 0,0,WEST



# Tests including ignoring the commands before it falls from  the table 

04_Ignore_before_Place.txt ->
- Verifies MOVE/LEFT/RIGHT/REPORT are ignored until a valid PLACE command is given  
- Expected :REPORT:- 0,0,NORTH

05_Boundary_Check.txt -> 
- Tests that MOVE is ignored when it would fall off the table (0,0,SOUTH), then turning LEFT allows movement  
- Expected: Report : - 0,0, South and 1,0, East 

06_Corner_Trap.txt ->
- Tests robot behaviour at table corner (4,4): invalid moves are ignored, then robot rotates and moves safely inside the grid  
- Expected: Report : - 4,3, South

07_Multiple_Place_Resets.txt -> 
- Tests that issuing a second PLACE resets robot position/direction, and movement continues from the new location
- Expected: Report : - 2,4, West

08_Ignore_invalid_Place_at_Boundary.txt
-  Long “stress test” combining multiple LEFT/RIGHT rotations with several MOVE commands to verify correct direction changes, position updates, and overall command sequencing  
- Expected: Report : - 1,4, West

09_Walk_Perimeter.txt  
- Perimeter/edge test: attempts to move 5 steps in each direction around the 5x5 grid, ensuring moves that would go off the table are ignored and the robot stays within bounds throughout  
- Expected: Report : - 0,0, West

10_invalid_place_then_valid.txt 
- Tests that an invalid PLACE command (outside the 5x5 grid) is ignored and subsequent commands are ignored until a valid PLACE is provided
- Expected: Report : - 2,1, EAST


