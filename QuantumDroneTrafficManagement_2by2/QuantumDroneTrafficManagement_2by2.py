class DroneGrid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.drones = {}

    def place_drone(self, drone, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] == ' ':
            if drone.name in self.drones:
                prev_row, prev_col = self.drones[drone.name].position
                self.grid[prev_row][prev_col] = ' '
            self.grid[row][col] = drone.name
            drone.place(row, col)
            self.drones[drone.name] = drone
            return True
        else:
            print(f"Invalid position for drone {drone.name}")
            return False

    def move_drone(self, drone, move_type, amount):
        if drone.name in self.drones:
            current_row, current_col = self.drones[drone.name].position
            new_position = drone.move(move_type, amount)

            if new_position is not False:
                new_row, new_col = new_position
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.grid[new_row][new_col] == ' ':
                    self.grid[current_row][current_col] = ' '
                    self.grid[new_row][new_col] = drone.name
                    drone.place(new_row, new_col)
                    return True
                else:
                    print(f"Invalid move for drone {drone.name}")
                    return False
            else:
                return False
        else:
            print(f"Drone {drone.name} not found")
            return False

    def display_grid(self):
        for row in self.grid:
            print('[{}] [{}]'.format(*row))
        
        print("")

    def is_drone(self, row, col):
        return self.grid[row][col] != ' ' if 0 <= row < self.rows and 0 <= col < self.cols else False

class Drone:
    def __init__(self, name):
        self.name = name
        self.position = None
        self.last_move_direction = None  # New attribute to track the last move direction

    def place(self, row, col):
        self.position = (row, col)

    def move(self, move_type, amount):
        row, col = self.position

        if move_type == 'vertical':
            row = (row + amount) % 2  # Wrap around for a 2x2 grid
        elif move_type == 'horizontal':
            col = (col + amount) % 2  # Wrap around for a 2x2 grid
        else:
            print("Invalid move type")
            return False

        self.last_move_direction = move_type  # Update the last move direction
        return row, col

    def get_position(self):
        return self.position

    def get_last_move(self):
        return self.last_move_direction