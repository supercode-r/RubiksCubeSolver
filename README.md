# RubiksCubeSolver
This Project Scans a 3x3x3 Rubik's cube using openCV and solves the cube using Two-phase Combinatorial Optimization method/ Deep Iterative A* search proposed by Kociemba. 

Please install the following requirements with your standard python packages. 

pip install numpy==1.19.4

pip install opencv-python==4.4.0.46

After satisfying the requirements, to run the solver type  

python gui.py 

Note: First run might take sometime to create all the manuevers' lookup table like moves, phase pruning 
