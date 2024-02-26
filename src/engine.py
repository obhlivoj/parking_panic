"""
engine.py

This module contains classes and functions for the Parking Panic game simulation.

Module Contents:
- read_txtfile: Reads the contents of a text file.
- menu: Displays the game menu and handles user input.
- Car: Car class to manage car attributes and movements.
- Parking: Class for managing the parking layout and functionalities.
- create_matrix: Creates the grid structure for the parking lot.
- input_cars: Adds cars to the parking grid.
- print_matrix: Prints the parking lot matrix.
- get_levels: Extracts level data from a text file.
- start_menu: Initializes the parking simulation with cars and records.
- read_recs: Reads the records from a text file.
- update_recs: Updates the records with the new moves for a specific level.
- start_intro_menu: Initializes the parking simulation with cars and records for the intro menu.
- engine_step: Performs a single step in the game.

Author: Vojtech Obhlidal
Year: 2023
"""



from typing import List, Dict, Tuple
from string import ascii_uppercase

COE  = '\u2500' # ─
CNS  = '\u2502' # │
CSE  = '\u250C' # ┌
CSO  = '\u2510' # ┐
CNE  = '\u2514' # └
CNO  = '\u2518' # ┘
CBLH = '\u2550' # ═
CBLV = '\u2551' # ║
CPAR = '\u2592' # ▒
ES = ' '
SA = '\n'


def read_txtfile(name: str) -> str:
    """Reads the contents of a text file.

    Args:
        name (str): The name of the text file.

    Returns:
        str: The contents of the text file.
    """
    try:
        with open(name, 'r', encoding='utf-8') as f:
            fstream=f.read()
        return fstream
    except FileNotFoundError as e:
        print(f'{e}')
        return ''

def menu(data_levels: List[List[str]]) -> int or None:
    """Displays the game menu and handles user input.

    Args:
        data_levels (List[List[str]]): A list of levels in the game.

    Returns:
        int or None: The level selected by the user, or None if an invalid level is selected.
    """
    f_records = read_txtfile('../data/records.txt')
    if not f_records:
        print('Welcome to Parking Panic. LEVEL 1 - RECORD 0 movements.')
        return 1

    data_record = f_records.split("\n")
    record_dicc = {}
    for r in data_record:
        r_split = r.split(' - ')
        try:
            record_dicc[r_split[0]] = r_split[1]
        except AttributeError:
            pass

    quest = 'Choose level ('
    for i in record_dicc:
        quest += i + '-'
    if int(list(record_dicc.keys())[-1]) <= len(data_levels):
        quest += str(int(list(record_dicc.keys())[-1])+1)
    quest += ')'
    x = input(quest)
    if x in list(record_dicc):
        pass
    elif int(x) == int(list(record_dicc.keys())[-1]) + 1:
        record_dicc[x] = 0
    else:
        print('This level is not available.')
        return None
    print('LEVEL ', x, ' ‐ RECORD',record_dicc[str(x)],'moves')
    return int(x)



class Car:
    """Car class to manage car attributes and movements."""

    def __init__(self, name: str, data: str = "0000"):
        """Initializes the car with given attributes.

        Args:
            name (str): Name of the car.
            data (str): Car data to initialize the car object.
        """
        self.name = name
        self.data = data
        self.parking = True
        self.dir = data[0]
        self.init_pos = [int(data[1]), int(data[2])]
        self.size = int(data[3])

        # Set initial car positions
        self.pos: List[List[int]] = [self.init_pos]
        for i in range(1, self.size):
            if self.dir == "H":
                self.pos.append([self.init_pos[0] + i, self.init_pos[1]])
            else:
                self.pos.append([self.init_pos[0], self.init_pos[1] + i])
        self.pos = self.pos[::-1]

    def copy_car(self) -> 'Car':
        """Creates a copy of the car object.

        Returns:
            Car: Copy of the car object.
        """
        car_copy = Car(self.name, self.data)
        car_copy.parking = self.parking
        for i, _ in enumerate(self.pos):
            car_copy.pos[i] = self.pos[i].copy()

        return car_copy

    def get_movement(self, direction: int) -> List[List[int]]:
        """Determines the movement of the car based on the given direction.

        Args:
            direction (int): 1 for forward, 0 for backward.

        Returns:
            List[List[int]]: A list of the new positions of the car.
        """

        moves = self.pos.copy()

        if self.dir == "H":
            if direction == 1:
                for i in range(len(self.pos)):
                    moves[i][0] += 1
            elif direction == 0:
                for i in range(len(self.pos)):
                    moves[i][0] -= 1
        else:
            if direction == 1:
                for i in range(len(self.pos)):
                    moves[i][1] += 1
            elif direction == 0:
                for i in range(len(self.pos)):
                    moves[i][1] -= 1

        return moves

    def move(self, direction: int) -> int:
        """Moves the car within the parking.

        Args:
            direction (int): 1 for forward, 0 for backward.
        
        Returns:
            int: 1 if the move was successful, 0 otherwise.
        """
        moves = self.get_movement(direction)

        out_of_parking = False
        if moves[0] == [7,3]:  # Check if the car is at the exit (if not victory).
            self.parking = False
        else:
            out_of_parking = any((pos[0] < 1 or pos[0] > 6) or (pos[1] < 1 or pos[1] > 6) for pos in moves)

        if not out_of_parking:
            self.pos = moves
            return 1
        return 0


class Parking:
    """This class defines a parking layout and its related functionalities."""

    def __init__(self, name: str):
        """Initialize a parking instance.

        Args:
            name (str): Name of the parking instance.
        """
        self.name = name
        self.victory = False
        self.size = 6
        self.grid: List[List[str]] = [["_" for _ in range(self.size)] for _ in range(self.size)]
        self.cars: List[Car] = []

    def update_grid(self) -> None:
        """Update the parking grid with the current positions of cars."""
        self.grid = [["_" for _ in range(self.size)] for _ in range(self.size)]
        for car in self.cars:
            self.grid[car.pos[0][1]-1][car.pos[0][0]-1] = (car.name).lower()
            for i in range(1, car.size):
                self.grid[car.pos[i][1]-1][car.pos[i][0]-1] = "x"
            self.grid[car.pos[-1][1]-1][car.pos[-1][0]-1] = (car.name).upper()

    def add_car(self, car: Car) -> None:
        """Add a car to the parking.

        Args:
            car (Car): Car instance to be added to the parking.
        """
        self.cars.append(car)

    def get_car_names(self) -> Dict[str, Car]:
        """Get names of all cars in the parking.

        Returns:
            Dict[str, Car]: A dictionary of car names and corresponding car objects.
        """
        names = [car.name for car in self.cars]
        names_dict = dict(zip(names, self.cars))
        return names_dict

    def move_car(self, movement: str, list_movements: List[str]) -> int:
        """Move a car in the parking.

        Args:
            movement (str): Movement command for the car.
            list_movements (List[str]): List of previous movements.

        Returns:
            int: A status code representing the result of the movement.
                Returns 1 if movement was successful, None otherwise.
        """
        if movement != "*":
            list_movements.append(movement)
        else:
            try:
                last_movement = list_movements[-1]
                movement = last_movement.upper() if last_movement.islower() else last_movement.lower()
                list_movements.pop()
            except IndexError:
                print("No movements to undo.")
                return None

        car_dir = int(movement.islower())
        car_name = movement.upper()
        names_dict = self.get_car_names()

        try:
            car = names_dict[car_name]
        except KeyError:
            print('That car does not exist.')
            return None

        virtual_car = car.copy_car()
        moved = virtual_car.move(car_dir)

        if not virtual_car.parking:
            self.victory = True
            del virtual_car
            return None

        if moved == 0:
            del virtual_car
            return None

        position = virtual_car.pos[car_dir-1]
        del virtual_car

        if self.grid[position[1]-1][position[0]-1] == '_':
            car.move(car_dir)
            self.update_grid()
            return 1
        return None


def create_matrix() -> List[List[str]]:
    """Creates the grid structure for the parking lot.
    
    Returns:
        List[List[str]]: A 2D matrix representing the parking lot layout.
    """
    matrix = [[" " for x in range(8*5)] for y in range(8*3)]

    h = len(matrix)
    w = len(matrix[0])
    for i in range(h):
        if (i <= 2) or (i >= h-3):
            for j in range(w):
                matrix[i][j] = CPAR
    for i in range(h):
        for j in range(w):
            if (j <= 4) or (j > w-6):
                matrix[i][j] = CPAR

    for i in range(h):
        for j in range(w):
            if 9 <= i <= 11:
                if j > w-6:
                    matrix[i][j] = " "
    return matrix

def input_cars(matrix: List[List[str]], parking: Parking) -> None:
    """Adds cars to the parking grid.
    
    Args:
        matrix (List[List[str]]): The parking lot layout.
        parking (Parking): The Parking instance with the cars.
    """
    for car in parking.cars:
        jump = 0
        p1 = [5 + car.pos[0][0]*5, car.pos[0][1]*3]
        p2 = [car.pos[-1][0]*5, car.pos[-1][1]*3]
        if car.dir == "H":
            jump = 2
            size = 4 + 5*(car.size-1)

            matrix[p1[1]][p1[0]-1] = CSO
            for i in range(1, jump):
                matrix[p1[1]+i][p1[0]-1] = CNS
            matrix[p1[1]+jump][p1[0]-1] = CNO

            matrix[p2[1]][p2[0]] = CSE
            for i in range(1, jump):
                matrix[p2[1]+i][p2[0]] = CNS
            matrix[p2[1]+jump][p2[0]] = CNE

            for i in (p1[1], p1[1]+jump):
                for j in range(1, size):
                    left = min(p1[0]-1, p2[0])
                    matrix[i][left+j] = COE

            matrix[p2[1]+1][p2[0]+2] = car.name
            matrix[p1[1]+1][p1[0]-3] = car.name.lower()

        else:
            jump = 4
            size = 2 + 3*(car.size-1)

            matrix[p1[1]+2][p1[0]-1] = CNO
            for j in range(1, jump):
                matrix[p1[1]+2][p1[0]-1-j] = COE
            matrix[p1[1]+2][p1[0]-1-4] = CNE

            matrix[p2[1]][p2[0]] = CSE
            for j in range(1, jump):
                matrix[p2[1]][p2[0]+j] = COE
            matrix[p2[1]][p2[0]+4] = CSO

            for j in (p1[0]-1, p1[0]-1-jump):
                for i in range(1, size):
                    left = min(p1[1]+2, p2[1])
                    matrix[left+i][j] = CNS

            matrix[p2[1]+1][p2[0]+2] = car.name
            matrix[p1[1]+1][p1[0]-3] = car.name.lower()


def print_matrix(matrix: List[List[str]]) -> None:
    """Prints the parking lot matrix.
    
    Args:
        matrix (List[List[str]]): The parking lot matrix to be printed.
    """
    with open('../data/res.txt', 'w', encoding='utf-8') as f:
        h = len(matrix)
        w = len(matrix[0])
        for i in range(h):
            line = ""
            for j in range(w):
                line += str(matrix[i][j])
            print(line)
            line += "\n"
            f.write(line)

def get_levels() -> List[List[str]]:
    """Extracts level data from a text file.
    
    Returns:
        List[List[str]]: A list of lists where each sublist represents the data for a particular level.
    """

    data_raw = read_txtfile('../data/levels.txt')
    data = data_raw.split("\n")
    n_levels = int(data[0])
    j=1
    data_levels = []
    for _ in range(n_levels):
        num_cars = int(data[j])
        list_cars = []
        for k in range(1, num_cars+1):
            list_cars.append(data[j+k])
        data_levels.append(list_cars)
        j = j+k+1

    return data_levels

def start_menu() -> Tuple[Parking, Dict[str, str], List[List[str]], List[str], int]:
    """Initializes the parking simulation with cars and records.

    Returns:
        Tuple[Parking, Dict[str, str], List[List[str]], List[str], int]: A tuple containing:
            - An instance of the Parking class with cars added.
            - A dictionary with records.
            - A parking lot matrix.
            - A list of car positions.
            - The selected level number.
    """
    # Possible car names.
    letters = list(ascii_uppercase)

    # Retrieve level data from text file.
    data_levels = get_levels()

    # Assume that menu is a function that accepts level data and returns a selected level.
    x = menu(data_levels)
    lvl = data_levels[x-1]

    # Read records from text file.
    f_records = read_txtfile("../data/records.txt")
    if not f_records:
        f_records = '1 - 0'
    data_record = f_records.split("\n")

    # Process records into dictionary.
    record_dicc = {}
    for r in data_record:
        r_split = r.split(' - ')
        try:
            record_dicc[r_split[0]] = r_split[1]
        except IndexError:
            pass

    # Create parking instance and add cars.
    park = Parking("park")
    for k, lvl_item in enumerate(lvl):
        car = Car(letters[k], lvl_item)
        park.add_car(car)
    park.update_grid()

    # Prepare parking lot matrix.
    matrix = create_matrix()
    input_cars(matrix, park)

    return park, record_dicc, matrix, lvl, x

def read_recs() -> dict:
    """Reads the records from a text file.

    Returns:
        dict: A dictionary containing the records.
    """
    f_records = read_txtfile("../data/records.txt")
    if not f_records:
        f_records = '1 - NOT SET'
    data_record = f_records.split("\n")

    # Process records into dictionary.
    record_dicc = {}
    for r in data_record:
        r_split = r.split(' - ')
        try:
            record_dicc[r_split[0]] = r_split[1]
        except IndexError:
            pass

    return record_dicc

def update_recs(moves: int, recs: dict, level: int) -> dict:
    """Updates the records with the new moves for a specific level.

    Args:
        moves (int): The new number of moves.
        recs (dict): The existing records.
        level (int): The level for which to update the records.

    Returns:
        dict: The updated records.
    """
    if recs[str(level)] == "NOT SET":
        recs[str(level)] = moves
    elif int(recs[str(level)]) > moves:
        recs[str(level)] = moves

    try:
        if recs[str(level+1)]:
            pass
    except IndexError:
        recs[str(level+1)] = "NOT SET"

    with open('../data/records.txt', 'w', encoding='utf-8') as f:
        for i in recs.keys():
            line = i + " - " + str(recs[i])
            line += "\n"
            f.write(line)

    return recs

def start_intro_menu(num_level: int) -> Tuple[Parking, List[List[str]], List[str]]:
    """Initializes the parking simulation with cars and records.

    Args:
        num_level (int): The level number to start the game with.

    Returns:
        Tuple[Parking, List[List[str]], List[str]]: A tuple containing:
            - An instance of the Parking class with cars added.
            - A parking lot matrix.
            - A list of car positions.

    The function performs the following tasks:
    - Retrieves level data from a text file based on the provided level number.
    - Creates an instance of the Parking class and adds cars based on the level data.
    - Updates the parking grid.
    - Prepares a parking lot matrix.
    """
    # Possible car names.
    letters = list(ascii_uppercase)

    # Retrieve level data from text file.
    data_levels = get_levels()
    lvl = data_levels[num_level-1]

    # Create parking instance and add cars.
    park = Parking("park")
    for k, lvl_item in enumerate(lvl):
        car = Car(letters[k], lvl_item)
        park.add_car(car)
    park.update_grid()

    # Prepare parking lot matrix.
    matrix = create_matrix()
    input_cars(matrix, park)

    return park, matrix, lvl

def engine_step(response: str, park: Parking, list_movements: list, moves: int) -> Tuple[int, int, int, List[List[str]]]:
    """Performs a single step in the game.

    Args:
        response (str): The movement command.
        park (Parking): The current state of the parking lot.
        list_movements (list): The list of previous movements.
        moves (int): The current number of moves.

    Returns:
        Tuple[int, int, int, List[List[str]]]: The success status of the movement,
                                                a flag indicating whether the game has been won,
                                                the updated number of moves,
                                                and the updated matrix.
    """
    success = 0
    moved = 0
    if response:
        mov = response
        for a in mov:
            moved = park.move_car(a, list_movements)
            if moved == 1:
                moves += 1

            if park.victory:
                moved = 1
                moves += 1
                success = 1
                break
        matrix = create_matrix()
        input_cars(matrix,park)
    else:
        matrix = None

    return moved, success, moves, matrix
