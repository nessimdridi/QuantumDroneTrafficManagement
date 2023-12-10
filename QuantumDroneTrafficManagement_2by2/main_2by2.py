import os
import time
from QuantumDroneTrafficManagement_2by2 import Drone, DroneGrid
import perceval as pcvl

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def move_drones(grid, drones, sampler):
    sample_count = sampler.sample_count(1)
    counts = sample_count['results']
    
    if counts[pcvl.BasicState([0,1,1,0])]==1:
        moveA = 'horizontal'
        moveB = 'horizontal'
    if counts[pcvl.BasicState([1,0,1,0])]==1:
        moveA = 'vertical'
        moveB = 'horizontal'
    if counts[pcvl.BasicState([1,0,0,1])]==1:
        moveA = 'vertical'
        moveB = 'vertical'
    if counts[pcvl.BasicState([0,1,0,1])]==1:
        moveA = 'horizontal'
        moveB = 'vertical'

    grid.move_drone(drones[0], moveA, 1)
    grid.move_drone(drones[1], moveB, 1)

def display_grid_and_last_move(grid, drones):
    clear_console()
    grid.display_grid()

    for drone in drones:
        last_move = drone.get_last_move()
        print(f'Last Move of {drone.name}: {last_move}')
    
    print("")

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"    --> Next move in {i} seconds.", end="\r")
        time.sleep(1)

def main():
    
    #UI INIT
    drone_A = Drone('A')
    drone_B = Drone('B')
    grid = DroneGrid(2, 2)  # 2x2 grid
    grid.place_drone(drone_A, 0, 0)
    grid.place_drone(drone_B, 1, 1)
    drones = [drone_A, drone_B]

    # CIRCUIT INIT
    circuit = pcvl.Circuit(4)
    circuit.add(0, pcvl.BS.H())
    circuit.add(2, pcvl.BS.H())
    p = pcvl.Processor("SLOS", circuit)
    bs1 = pcvl.BasicState([0,1,1,0])
    bs2 = pcvl.BasicState([1, 0, 0, 1])
    input_state = bs1-bs2               
    p.with_input(input_state)
    sampler = pcvl.algorithm.Sampler(p)

    try:
        while True:
            move_drones(grid, drones, sampler)
            display_grid_and_last_move(grid, drones)
            countdown_timer(3)
    except KeyboardInterrupt:
        print("\nScript interrupted.")

if __name__ == "__main__":
    main()
