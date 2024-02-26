import pytest
from engine import Car, Parking, create_matrix, get_levels

def test_Car():
    car = Car('A', '1000')
    assert car.name == 'A'
    assert car.data == '1000'

def test_Car_copy_car():
    car = Car('A', '1000')
    car_copy = car.copy_car()
    assert car.name == car_copy.name
    assert car.data == car_copy.data

def test_Parking():
    parking = Parking('park1')
    assert parking.name == 'park1'

def test_Parking_update_grid():
    parking = Parking('park1')
    car = Car('A', '1000')
    parking.add_car(car)
    parking.update_grid()
    assert 'A' in parking.grid[car.pos[0][1]-1]

def test_create_matrix():
    matrix = create_matrix()
    assert len(matrix) == 8*3
    assert len(matrix[0]) == 8*5

def test_get_levels():
    data_levels = get_levels()
    assert isinstance(data_levels, list)
    assert isinstance(data_levels[0], list)
    assert isinstance(data_levels[0][0], str)

