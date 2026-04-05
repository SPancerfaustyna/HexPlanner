import pytest

from hexplanner.model import tile_data


def test_tile_data_stores_type_road_and_height():
	data = tile_data.TileData(tile_type=3, has_road=True, height=42)

	assert data.tile_type == 3
	assert data.has_road is True
	assert data.height == 42


@pytest.mark.parametrize("tile_type", [0, 1, 7, 15])
def test_tile_data_accepts_valid_tile_type_range(tile_type):
	data = tile_data.TileData(tile_type=tile_type, has_road=False, height=0)

	assert data.tile_type == tile_type


@pytest.mark.parametrize("tile_type", [-1, 16, 999])
def test_tile_data_rejects_invalid_tile_type_range(tile_type):
	with pytest.raises(ValueError):
		tile_data.TileData(tile_type=tile_type, has_road=False, height=0)


@pytest.mark.parametrize("invalid_value", ["1", None, 1.5, True])
def test_tile_data_rejects_non_int_tile_type_values(invalid_value):
	with pytest.raises(TypeError):
		tile_data.TileData(tile_type=invalid_value, has_road=False, height=0)


@pytest.mark.parametrize("has_road", [True, False])
def test_tile_data_accepts_valid_road_values(has_road):
	data = tile_data.TileData(tile_type=1, has_road=has_road, height=0)

	assert data.has_road == has_road


@pytest.mark.parametrize("invalid_value", [0, 1, "true", None])
def test_tile_data_rejects_non_bool_road_values(invalid_value):
	with pytest.raises(TypeError):
		tile_data.TileData(tile_type=1, has_road=invalid_value, height=0)


@pytest.mark.parametrize("height", [0, 1, 127, 255])
def test_tile_data_accepts_valid_height_range(height):
	data = tile_data.TileData(tile_type=1, has_road=False, height=height)

	assert data.height == height


@pytest.mark.parametrize("height", [-1, 256, 999])
def test_tile_data_rejects_invalid_height_range(height):
	with pytest.raises(ValueError):
		tile_data.TileData(tile_type=1, has_road=False, height=height)


@pytest.mark.parametrize("invalid_value", ["1", None, 1.5, True])
def test_tile_data_rejects_non_int_height_values(invalid_value):
	with pytest.raises(TypeError):
		tile_data.TileData(tile_type=1, has_road=False, height=invalid_value)
