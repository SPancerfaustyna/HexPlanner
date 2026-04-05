import pytest

from hexplanner.model import tile_bits

# Type tests
@pytest.mark.parametrize("value", [0, 1, 5, 10, 15])
def test_set_and_get_type(value):
    meta = tile_bits.set_type(0, value)
    assert tile_bits.get_type(meta) == value

@pytest.mark.parametrize("old_value, new_value", [
    (0, 3),
    (1, 7),
    (5, 10),
    (10, 15),
    (15, 0)
    ])
def test_set_type_overwrites_previous(old_value, new_value):
    meta = tile_bits.set_type(0, old_value)
    meta = tile_bits.set_type(meta, new_value)
    assert tile_bits.get_type(meta) == new_value

def test_set_type_accepts_max_valid_value():
    meta = tile_bits.set_type(0, 15)
    assert tile_bits.get_type(meta) == 15

@pytest.mark.parametrize("invalid_value", [-1, 16, 255])
def test_set_type_invalid_value(invalid_value):
    meta = 0
    with pytest.raises(ValueError):
        tile_bits.set_type(meta, invalid_value)

@pytest.mark.parametrize("invalid_value_type", ["not an int", None])
def test_set_type_invalid_value_type(invalid_value_type):
    meta = 0
    with pytest.raises(TypeError):
        tile_bits.set_type(meta, invalid_value_type)

def test_clear_type():
    meta = tile_bits.set_type(0, 5)
    meta = tile_bits.clear_type(meta)
    assert tile_bits.get_type(meta) == 0

# Road tests
@pytest.mark.parametrize("has_road", [True, False])
def test_set_and_has_road(has_road):
    meta = tile_bits.set_road(0, has_road)
    assert tile_bits.has_road(meta) == has_road

def test_set_road_overwrites_previous():
    meta = tile_bits.set_road(0, True)
    meta = tile_bits.set_road(meta, False)
    assert tile_bits.has_road(meta) == False

@pytest.mark.parametrize("has_road", [True, False])
def test_toggle_road(has_road):
    meta = tile_bits.set_road(0, has_road)
    meta = tile_bits.toggle_road(meta)
    assert tile_bits.has_road(meta) == (not has_road)

def test_clear_road():
    meta = tile_bits.set_road(0, True)
    meta = tile_bits.clear_road(meta)
    assert tile_bits.has_road(meta) == False

@pytest.mark.parametrize("invalid_value", ["not a bool", None])
def test_set_road_invalid_value_type(invalid_value):
    meta = 0
    with pytest.raises(TypeError):
        tile_bits.set_road(meta, invalid_value)

# Independent tests
def test_road_does_not_affect_type():
    meta = tile_bits.set_type(0, 5)
    meta = tile_bits.set_road(meta, True)
    assert tile_bits.get_type(meta) == 5

def test_type_does_not_affect_road():
    meta = tile_bits.set_road(0, True)
    meta = tile_bits.set_type(meta, 5)
    assert tile_bits.has_road(meta) == True

def test_clear_type_does_not_affect_road():
    meta = tile_bits.set_type(0, 5)
    meta = tile_bits.set_road(meta, True)
    meta = tile_bits.clear_type(meta)
    assert tile_bits.get_type(meta) == 0
    assert tile_bits.has_road(meta) == True

def test_clear_road_does_not_affect_type():
    meta = tile_bits.set_type(0, 5)
    meta = tile_bits.set_road(meta, True)
    meta = tile_bits.clear_road(meta)
    assert tile_bits.get_type(meta) == 5
    assert tile_bits.has_road(meta) == False

# All bits tests
def test_clear_all():
    meta = tile_bits.set_type(0, 5)
    meta = tile_bits.set_road(meta, True)
    meta = tile_bits.clear_all(meta)
    assert tile_bits.get_type(meta) == 0
    assert tile_bits.has_road(meta) == False

# Pack tests
@pytest.mark.parametrize("tile_type, has_road", [
    (0, False),
    (5, True),
    (10, False),
    (15, True)
])
def test_pack(tile_type, has_road):
    meta = tile_bits.pack(tile_type, has_road)
    assert tile_bits.get_type(meta) == tile_type
    assert tile_bits.has_road(meta) == has_road

@pytest.mark.parametrize("tile_type, has_road", [
    (0, False),
    (5, True),
    (10, False),
    (15, True)
])
def test_unpack(tile_type, has_road):
    meta = tile_bits.pack(tile_type, has_road)
    unpacked_type, unpacked_has_road = tile_bits.unpack(meta)
    assert unpacked_type == tile_type
    assert unpacked_has_road == has_road
