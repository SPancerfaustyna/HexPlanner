import pytest

from hexplanner.model import big_tile_data

# stores type, road and height, coords
def test_tile_data_stores_type_road_height_and_coords():
    data = big_tile_data.BigTileData(tile_type_id=3, has_road=True, height=42, x=5, y=10)

    assert data.tile_type_id == 3
    assert data.has_road is True
    assert data.height == 42
    assert data.x == 5
    assert data.y == 10

def test_creation_and_get_tile_type():
    data = big_tile_data.BigTileData(tile_type_id=3, has_road=True, height=42, x=0, y=0)
    assert data.tile_type_id == 3

@pytest.mark.parametrize("tile_type_id", [0, 1, 7, 15])
def test_tile_data_accepts_valid_tile_type_range(tile_type_id):
    data = big_tile_data.BigTileData(tile_type_id=tile_type_id, has_road=False, height=0, x=0, y=0)
    assert data.tile_type_id == tile_type_id

@pytest.mark.parametrize("tile_type_id", [-1, 16, 999])
def test_tile_data_rejects_invalid_tile_type_range(tile_type_id):
    with pytest.raises(ValueError):
        big_tile_data.BigTileData(tile_type_id=tile_type_id, has_road=False, height=0, x=0, y=0)

@pytest.mark.parametrize("invalid_value", ["1", None, 1.5, True])
def test_tile_data_rejects_non_int_tile_type_values(invalid_value):
    with pytest.raises(TypeError):
        big_tile_data.BigTileData(tile_type_id=invalid_value, has_road=False, height=0, x=0, y=0)


def test_creation_and_get_road_flag():
    data = big_tile_data.BigTileData(tile_type_id=3, has_road=True, height=42, x=5, y=10)
    assert data.has_road is True

@pytest.mark.parametrize("has_road", [True, False])
def test_tile_data_accepts_valid_road_values(has_road):
    data = big_tile_data.BigTileData(tile_type_id=1, has_road=has_road, height=0, x=0, y=0)
    assert data.has_road == has_road

@pytest.mark.parametrize("invalid_value", [0, 1, "true", None])
def test_tile_data_rejects_non_bool_road_values(invalid_value):
    with pytest.raises(TypeError):
        big_tile_data.BigTileData(tile_type_id=1, has_road=invalid_value, height=0, x=0, y=0)


def test_creation_and_get_height():
    data = big_tile_data.BigTileData(tile_type_id=3, has_road=True, height=42, x=5, y=10)
    assert data.height == 42

@pytest.mark.parametrize("height", [0, 1, 127, 255])
def test_tile_data_accepts_valid_height_range(height):
    data = big_tile_data.BigTileData(tile_type_id=1, has_road=False, height=height, x=0, y=0)
    assert data.height == height

@pytest.mark.parametrize("height", [-1, 256, 999])
def test_tile_data_rejects_invalid_height_range(height):
    with pytest.raises(ValueError):
        big_tile_data.BigTileData(tile_type_id=1, has_road=False, height=height, x=0, y=0)

@pytest.mark.parametrize("invalid_value", ["1", None, 1.5, True])
def test_tile_data_rejects_non_int_height_values(invalid_value):
    with pytest.raises(TypeError):
        big_tile_data.BigTileData(tile_type_id=1, has_road=False, height=invalid_value, x=0, y=0)


def test_creation_and_get_x_coords():
    data = big_tile_data.BigTileData(tile_type_id=3, has_road=True, height=42, x=5, y=10)
    assert data.x == 5

def test_creation_and_get_y_coords():
    data = big_tile_data.BigTileData(tile_type_id=3, has_road=True, height=42, x=5, y=10)
    assert data.y == 10

@pytest.mark.parametrize("x", [0, 1, 10, 100])
def test_tile_data_accepts_valid_x_coords(x):
    data = big_tile_data.BigTileData(tile_type_id=1, has_road=False, height=0, x=x, y=0)
    assert data.x == x

@pytest.mark.parametrize("y", [0, 1, 10, 100])
def test_tile_data_accepts_valid_y_coords(y):
    data = big_tile_data.BigTileData(tile_type_id=1, has_road=False, height=0, x=0, y=y)
    assert data.y == y

@pytest.mark.parametrize("invalid_value", ["1", None, 1.5, True])
def test_tile_data_rejects_invalid_type_coords(invalid_value):
    with pytest.raises(TypeError):
        big_tile_data.BigTileData(tile_type_id=1, has_road=False, height=0, x=invalid_value, y=0)
    with pytest.raises(TypeError):
        big_tile_data.BigTileData(tile_type_id=1, has_road=False, height=0, x=0, y=invalid_value)


def test_tile_data_frozen():
    import dataclasses

    data = big_tile_data.BigTileData(tile_type_id=3, has_road=True, height=42, x=5, y=10)
    with pytest.raises(dataclasses.FrozenInstanceError):
        data.tile_type_id = 1
    with pytest.raises(dataclasses.FrozenInstanceError):
        data.has_road = False
    with pytest.raises(dataclasses.FrozenInstanceError):
        data.height = 0
    with pytest.raises(dataclasses.FrozenInstanceError):
        data.x = 0
    with pytest.raises(dataclasses.FrozenInstanceError):
        data.y = 0
    
