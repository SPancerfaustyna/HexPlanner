import pytest

from hexplanner.model import tile_types

DEFAULT_TILE_TYPE_NAMES = (
    "Other",
    "Water",
    "Land",
    "Mountain",
    "Coastal district",

    "Traders district",
    "Main plaza",
    "Hunting district",
    "Smithing district",
    "Masonry district",
    
    "Farming district",
    "Woodcutting district",
    "Tailoring district",
    "Housing district",
    "Scholar district",
    
    "Cooking district"
)

DEFAULT_TILE_TYPE_COLORS = (
    "#252525",
    "#006EFF",
    "#118011",
    "#6B8561",
    "#000005",
    
    "#000006",
    "#000007",
    "#000008",
    "#000009",
    "#000010",
    
    "#000011",
    "#000012",
    "#000013",
    "#000014",
    "#000015",
    
    "#000016"
)

DEFAULT_TILE_TYPE_ROAD_FLAGS = (
    False,
    False,
    True,
    False,
    True,
    
    True,
    True,
    True,
    True,
    True,
    
    True,
    True,
    True,
    True,
    True,
    
    True
)

NOT_INT_VALUES = [None, 3.14, "not an int", True]
NOT_STR_VALUES = [None, 3.14, True, 123]
NOT_BOOL_VALUES = [None, 3.14, "not a bool", 123]
NOT_LIST_VALUES = [None, 3.14, "not a list", True, 123, {"not": "a list"}]
NOT_DICT_VALUES = [None, 3.14, "not a dict", True, 123, ["not", "a", "dict"]]

VALID_ID_VALUES = list(range(len(DEFAULT_TILE_TYPE_NAMES)))
INVALID_ID_VALUES = [100, -1, 999]

@pytest.fixture(autouse=True)
def tile_types_fixture():
    tile_types_instance = tile_types.TileTypes()
    return tile_types_instance

"""========================
        Names
========================"""

# ===== get name =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_get_name(tile_types_fixture, type_id):
    assert tile_types_fixture.get_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_get_name_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.get_name(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_get_name_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.get_name(type_id=type_id)

# ===== get names =====
def test_get_names(tile_types_fixture):
    names = tile_types_fixture.get_names()
    names_expected = list(DEFAULT_TILE_TYPE_NAMES)
    assert len(names) == len(names_expected)
    assert names == names_expected

# ===== overwrite name =====
@pytest.mark.parametrize("type_id, new_name", [
    (0, "New Other"),
    (1, "New Water"),
    (2, "New Land"),
    (3, "New Mountain"),
    (10, "New Farming district"),
])
def test_overwrite_name(tile_types_fixture, type_id, new_name):
    tile_types_fixture.overwrite_name(type_id=type_id, new_name=new_name)
    assert tile_types_fixture.get_name(type_id=type_id) == new_name

def test_overwrite_name_not_affect_other_names(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_name(type_id=1, new_name="New Water")

    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_name(type_id=1) == "New Water"
    assert tile_types_fixture.get_name(type_id=2) == DEFAULT_TILE_TYPE_NAMES[2]

def test_overwrite_name_not_affect_color_or_road_flag(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")

    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_color(type_id=0) == DEFAULT_TILE_TYPE_COLORS[0]
    assert tile_types_fixture.get_road_flag(type_id=0) == DEFAULT_TILE_TYPE_ROAD_FLAGS[0]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_overwrite_name_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_name(type_id=type_id, new_name="Invalid ID")

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_overwrite_name_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_name(type_id=type_id, new_name="Invalid ID")

@pytest.mark.parametrize("new_name", NOT_STR_VALUES)
def test_overwrite_name_invalid_name_type(tile_types_fixture, new_name):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_name(type_id=0, new_name=new_name)

# ===== overwrite names =====
def test_overwrite_names(tile_types_fixture):
    new_names = [
        "New Other",
        "New Water",
        "New Land",
        "New Mountain",

        "New Coastal district",
        "New Traders district",
        "New Main plaza",
        "New Hunting district",
        "New Smithing district",
        "New Masonry district",
        "New Farming district",
        "New Woodcutting district",
        "New Tailoring district",
        "New Housing district",
        "New Scholar district",
        "New Cooking district"
    ]
    tile_types_fixture.overwrite_names(new_names=new_names)
    names = tile_types_fixture.get_names()
    assert len(names) == len(new_names)
    assert names == new_names

def test_overwrite_names_not_affect_color_or_road_flag(tile_types_fixture):
    new_names = [
        "New Other",
        "New Water",
        "New Land",
        "New Mountain",

        "New Coastal district",
        "New Traders district",
        "New Main plaza",
        "New Hunting district",
        "New Smithing district",
        "New Masonry district",
        "New Farming district",
        "New Woodcutting district",
        "New Tailoring district",
        "New Housing district",
        "New Scholar district",
        "New Cooking district"
    ]
    tile_types_fixture.overwrite_names(new_names=new_names)

    for type_id in range(len(new_names)):
        assert tile_types_fixture.get_name(type_id=type_id) == new_names[type_id]
        assert tile_types_fixture.get_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]
        assert tile_types_fixture.get_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

@pytest.mark.parametrize("new_names", NOT_LIST_VALUES)
def test_overwrite_names_invalid_type(tile_types_fixture, new_names):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_names(new_names=new_names)

@pytest.mark.parametrize("new_names", [
    ["New Other", "New Water"],  # too short
    ["New Other"] * 16 + ["Extra Name"],  # too long
])
def test_overwrite_names_invalid_length(tile_types_fixture, new_names):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_names(new_names=new_names)

def test_overwrite_names_invalid_type_in_list(tile_types_fixture):
    new_names = ["New Other", "New Water", "New Land", "New Mountain"] + [123] * 12
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_names(new_names=new_names)

# ===== overwrite names dict =====
def test_overwrite_names_dict(tile_types_fixture):
    new_names_dict = {
        0: "New Other",
        1: "New Water",
        2: "New Land",
        3: "New Mountain",
        10: "New Farming district"
    }
    tile_types_fixture.overwrite_names_dict(new_names_dict=new_names_dict)
    for type_id, new_name in new_names_dict.items():
        assert tile_types_fixture.get_name(type_id=type_id) == new_name

def test_overwrite_names_dict_not_affect_other_names(tile_types_fixture):
    new_names_dict = {
        0: "New Other",
        1: "New Water",
        2: "New Land",
        3: "New Mountain",
        10: "New Farming district"
    }
    tile_types_fixture.overwrite_names_dict(new_names_dict=new_names_dict)

    for type_id in range(len(DEFAULT_TILE_TYPE_NAMES)):
        if type_id in new_names_dict:
            assert tile_types_fixture.get_name(type_id=type_id) == new_names_dict[type_id]
        else:
            assert tile_types_fixture.get_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]

def test_overwrite_names_dict_not_affect_color_or_road_flag(tile_types_fixture):
    new_names_dict = {
        0: "New Other",
        1: "New Water",
        2: "New Land",
        3: "New Mountain",
        10: "New Farming district"
    }
    tile_types_fixture.overwrite_names_dict(new_names_dict=new_names_dict)

    for type_id in range(len(DEFAULT_TILE_TYPE_NAMES)):
        assert tile_types_fixture.get_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]
        assert tile_types_fixture.get_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

@pytest.mark.parametrize("new_names_dict", NOT_DICT_VALUES)
def test_overwrite_names_dict_invalid_type(tile_types_fixture, new_names_dict):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_names_dict(new_names_dict=new_names_dict)

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_overwrite_names_dict_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_names_dict(new_names_dict={type_id: "type name"})

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_overwrite_names_dict_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_names_dict(new_names_dict={type_id: "type name"})

@pytest.mark.parametrize("new_name", NOT_STR_VALUES)
def test_overwrite_names_dict_invalid_name_type(tile_types_fixture, new_name):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_names_dict(new_names_dict={0: new_name})

# ===== get default name =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_get_default_name(tile_types_fixture, type_id):
    assert tile_types_fixture.get_default_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_get_default_name_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.get_default_name(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_get_default_name_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.get_default_name(type_id=type_id)

# ===== get default names =====
def test_get_default_names(tile_types_fixture):
    default_names = tile_types_fixture.get_default_names()
    assert len(default_names) == len(DEFAULT_TILE_TYPE_NAMES)
    assert default_names == DEFAULT_TILE_TYPE_NAMES

# ===== to default name =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_to_default_name(tile_types_fixture, type_id):
    tile_types_fixture.overwrite_name(type_id=type_id, new_name="New Name")

    tile_types_fixture.to_default_name(type_id=type_id)

    assert tile_types_fixture.get_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]

def test_to_default_name_not_affect_other_names(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_name(type_id=1, new_name="New Water")

    tile_types_fixture.to_default_name(type_id=0)

    assert tile_types_fixture.get_name(type_id=0) == DEFAULT_TILE_TYPE_NAMES[0]
    assert tile_types_fixture.get_name(type_id=1) == "New Water"

def test_to_default_name_not_affect_color_or_road_flag(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)

    tile_types_fixture.to_default_name(type_id=0)

    assert tile_types_fixture.get_name(type_id=0) == DEFAULT_TILE_TYPE_NAMES[0]
    assert tile_types_fixture.get_color(type_id=0) == "#123456"
    assert tile_types_fixture.get_road_flag(type_id=0) == False

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_to_default_name_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.to_default_name(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_to_default_name_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.to_default_name(type_id=type_id)

# ===== to default names =====
def test_to_default_names(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_name(type_id=1, new_name="New Water")

    tile_types_fixture.to_default_names()

    assert tile_types_fixture.get_name(type_id=0) == DEFAULT_TILE_TYPE_NAMES[0]
    assert tile_types_fixture.get_name(type_id=1) == DEFAULT_TILE_TYPE_NAMES[1]

def test_to_default_names_not_affect_color_or_road_flag(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_name(type_id=1, new_name="New Water")
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=False)

    tile_types_fixture.to_default_names()

    assert tile_types_fixture.get_color(type_id=0) == "#123456"
    assert tile_types_fixture.get_color(type_id=1) == DEFAULT_TILE_TYPE_COLORS[1]
    assert tile_types_fixture.get_road_flag(type_id=0) == DEFAULT_TILE_TYPE_ROAD_FLAGS[0]
    assert tile_types_fixture.get_road_flag(type_id=1) == False


"""========================
        Colors
========================"""

# ===== get color =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_get_color(tile_types_fixture, type_id):
    assert tile_types_fixture.get_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_get_color_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.get_color(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_get_color_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.get_color(type_id=type_id)

# ===== get colors =====
def test_get_colors(tile_types_fixture):
    colors = tile_types_fixture.get_colors()
    colors_expected = list(DEFAULT_TILE_TYPE_COLORS)
    assert len(colors) == len(colors_expected)
    assert colors == colors_expected

# ===== overwrite color =====
@pytest.mark.parametrize("type_id, new_color", [
    (0, "#123456"),
    (1, "#654321"),
    (5, "#ABCDEF"),
    (9, "#FEDCBA"),
    (14, "#0F0F0F")
])
def test_overwrite_color(tile_types_fixture, type_id, new_color):
    tile_types_fixture.overwrite_color(type_id=type_id, new_color=new_color)
    assert tile_types_fixture.get_color(type_id=type_id) == new_color

def test_overwrite_color_not_affect_other_colors(tile_types_fixture):
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#654321")

    assert tile_types_fixture.get_color(type_id=0) == "#123456"
    assert tile_types_fixture.get_color(type_id=1) == "#654321"
    assert tile_types_fixture.get_color(type_id=2) == DEFAULT_TILE_TYPE_COLORS[2]

def test_overwrite_color_not_affect_name_or_road_flag(tile_types_fixture):
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")

    assert tile_types_fixture.get_color(type_id=0) == "#123456"
    assert tile_types_fixture.get_name(type_id=0) == DEFAULT_TILE_TYPE_NAMES[0]
    assert tile_types_fixture.get_road_flag(type_id=0) == DEFAULT_TILE_TYPE_ROAD_FLAGS[0]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_overwrite_color_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_color(type_id=type_id, new_color="#123456")

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_overwrite_color_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_color(type_id=type_id, new_color="#123456")

@pytest.mark.parametrize("new_color", NOT_STR_VALUES)
def test_overwrite_color_invalid_color_type(tile_types_fixture, new_color):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_color(type_id=0, new_color=new_color)

@pytest.mark.parametrize("new_color", ["#12345", "#1234567", "123456", "#ZZZZZZ"])
def test_overwrite_color_invalid_format(tile_types_fixture, new_color):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_color(type_id=0, new_color=new_color)

# ===== overwrite colors =====
def test_overwrite_colors(tile_types_fixture):
    new_colors = [
        "#123456",
        "#654321",
        "#ABCDEF",
        "#FEDCBA",
        "#0F0F0F",
        "#111111",
        "#222222",
        "#333333",
        "#444444",
        "#555555",
        "#666666",
        "#777777",
        "#888888",
        "#999999",
        "#AAAAAA",
        "#BBBBBB"
    ]
    tile_types_fixture.overwrite_colors(new_colors=new_colors)
    colors = tile_types_fixture.get_colors()
    assert len(colors) == len(new_colors)
    assert colors == new_colors

def test_overwrite_colors_not_affect_name_or_road_flag(tile_types_fixture):
    new_colors = [
        "#123456",
        "#654321",
        "#ABCDEF",
        "#FEDCBA",
        "#0F0F0F",
        "#111111",
        "#222222",
        "#333333",
        "#444444",
        "#555555",
        "#666666",
        "#777777",
        "#888888",
        "#999999",
        "#AAAAAA",
        "#BBBBBB"
    ]
    tile_types_fixture.overwrite_colors(new_colors=new_colors)

    for type_id in range(len(new_colors)):
        assert tile_types_fixture.get_color(type_id=type_id) == new_colors[type_id]
        assert tile_types_fixture.get_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]
        assert tile_types_fixture.get_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

@pytest.mark.parametrize("new_colors", NOT_LIST_VALUES)
def test_overwrite_colors_invalid_type(tile_types_fixture, new_colors):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_colors(new_colors=new_colors)

@pytest.mark.parametrize("new_colors", [
    ["#123456", "#654321"],  # too short
    ["#123456"] * 15 + ["#1234567"],  # too long
])
def test_overwrite_colors_invalid_length(tile_types_fixture, new_colors):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_colors(new_colors=new_colors)

def test_overwrite_colors_invalid_type_in_list(tile_types_fixture):
    new_colors = ["#123456", "#654321", "#ABCDEF", "#FEDCBA"] + [123] * 12
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_colors(new_colors=new_colors)

@pytest.mark.parametrize("new_color", [
    "#12345", "#1234567", "123456", "#ZZZZZZ"
])
def test_overwrite_colors_invalid_format_in_list(tile_types_fixture, new_color):
    new_colors_list = ["#123456", "#654321", "#ABCDEF", "#FEDCBA"] + [new_color] * 12
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_colors(new_colors=new_colors_list)

# ===== overwrite colors dict =====
def test_overwrite_colors_dict(tile_types_fixture):
    new_colors_dict = {
        0: "#123456",
        1: "#654321",
        2: "#ABCDEF",
        3: "#FEDCBA",
        10: "#0F0F0F"
    }
    tile_types_fixture.overwrite_colors_dict(new_colors_dict=new_colors_dict)
    for type_id, new_color in new_colors_dict.items():
        assert tile_types_fixture.get_color(type_id=type_id) == new_color

def test_overwrite_colors_dict_not_affect_other_colors(tile_types_fixture):
    new_colors_dict = {
        0: "#123456",
        1: "#654321",
        2: "#ABCDEF",
        3: "#FEDCBA",
        10: "#0F0F0F"
    }
    tile_types_fixture.overwrite_colors_dict(new_colors_dict=new_colors_dict)

    for type_id in range(len(DEFAULT_TILE_TYPE_COLORS)):
        if type_id in new_colors_dict:
            assert tile_types_fixture.get_color(type_id=type_id) == new_colors_dict[type_id]
        else:
            assert tile_types_fixture.get_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]

def test_overwrite_colors_dict_not_affect_name_or_road_flag(tile_types_fixture):
    new_colors_dict = {
        0: "#123456",
        1: "#654321",
        2: "#ABCDEF",
        3: "#FEDCBA",
        10: "#0F0F0F"
    }
    tile_types_fixture.overwrite_colors_dict(new_colors_dict=new_colors_dict)

    for type_id in range(len(DEFAULT_TILE_TYPE_COLORS)):
        assert tile_types_fixture.get_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]
        assert tile_types_fixture.get_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

@pytest.mark.parametrize("new_colors_dict", NOT_DICT_VALUES)
def test_overwrite_colors_dict_invalid_type(tile_types_fixture, new_colors_dict):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_colors_dict(new_colors_dict=new_colors_dict)

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_overwrite_colors_dict_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_colors_dict(new_colors_dict={type_id: "#123456"})

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_overwrite_colors_dict_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_colors_dict(new_colors_dict={type_id: "#123456"})

@pytest.mark.parametrize("new_color", NOT_STR_VALUES)
def test_overwrite_colors_dict_invalid_color_type(tile_types_fixture, new_color):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_colors_dict(new_colors_dict={0: new_color})

@pytest.mark.parametrize("new_color", ["#12345", "#1234567", "123456", "#ZZZZZZ"])
def test_overwrite_colors_dict_invalid_color_format(tile_types_fixture, new_color):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_colors_dict(new_colors_dict={0: new_color})


# ===== get default color =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_get_default_color(tile_types_fixture, type_id):
    assert tile_types_fixture.get_default_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_get_default_color_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.get_default_color(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_get_default_color_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.get_default_color(type_id=type_id)

# ===== get default colors =====
def test_get_default_colors(tile_types_fixture):
    default_colors = tile_types_fixture.get_default_colors()
    assert len(default_colors) == len(DEFAULT_TILE_TYPE_COLORS)
    assert default_colors == DEFAULT_TILE_TYPE_COLORS

# ===== to default color =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_to_default_color(tile_types_fixture, type_id):
    tile_types_fixture.overwrite_color(type_id=type_id, new_color="#123456")

    tile_types_fixture.to_default_color(type_id=type_id)

    assert tile_types_fixture.get_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]

def test_to_default_color_not_affect_other_colors(tile_types_fixture):
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#654321")

    tile_types_fixture.to_default_color(type_id=0)

    assert tile_types_fixture.get_color(type_id=0) == DEFAULT_TILE_TYPE_COLORS[0]
    assert tile_types_fixture.get_color(type_id=1) == "#654321"

def test_to_default_color_not_affect_name_or_road_flag(tile_types_fixture):
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)

    tile_types_fixture.to_default_color(type_id=0)

    assert tile_types_fixture.get_color(type_id=0) == DEFAULT_TILE_TYPE_COLORS[0]
    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_road_flag(type_id=0) == False

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_to_default_color_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.to_default_color(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_to_default_color_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.to_default_color(type_id=type_id)

# ===== to default colors =====
def test_to_default_colors(tile_types_fixture):
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#654321")

    tile_types_fixture.to_default_colors()

    assert tile_types_fixture.get_color(type_id=0) == DEFAULT_TILE_TYPE_COLORS[0]
    assert tile_types_fixture.get_color(type_id=1) == DEFAULT_TILE_TYPE_COLORS[1]

def test_to_default_colors_not_affect_name_or_road_flag(tile_types_fixture):
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#654321")
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=False)

    tile_types_fixture.to_default_colors()

    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_road_flag(type_id=1) == False

"""========================
        Road flags
========================"""

# ===== get road flag =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_get_road_flag(tile_types_fixture, type_id):
    assert tile_types_fixture.get_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_get_road_flag_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.get_road_flag(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_get_road_flag_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.get_road_flag(type_id=type_id)

# ===== get road flags =====
def test_get_road_flags(tile_types_fixture):
    road_flags = tile_types_fixture.get_road_flags()
    road_flags_expected = list(DEFAULT_TILE_TYPE_ROAD_FLAGS)
    assert len(road_flags) == len(road_flags_expected)
    assert road_flags == road_flags_expected

# ===== overwrite road flag =====
@pytest.mark.parametrize("type_id, can_have_road", [
    (0, True),
    (1, True),
    (6, False),
    (13, True),
])
def test_overwrite_road_flag(tile_types_fixture, type_id, can_have_road):
    tile_types_fixture.overwrite_road_flag(type_id=type_id, road_flag=can_have_road)
    assert tile_types_fixture.get_road_flag(type_id=type_id) == can_have_road

def test_overwrite_road_flag_not_affect_other_flags(tile_types_fixture):
    tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=True)
    tile_types_fixture.overwrite_road_flag(type_id=2, road_flag=False)

    assert tile_types_fixture.get_road_flag(type_id=1) == True
    assert tile_types_fixture.get_road_flag(type_id=2) == False
    assert tile_types_fixture.get_road_flag(type_id=3) == DEFAULT_TILE_TYPE_ROAD_FLAGS[3]

def test_overwrite_road_flag_not_affect_name_or_color(tile_types_fixture):
    tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=True)

    assert tile_types_fixture.get_road_flag(type_id=1) == True
    assert tile_types_fixture.get_name(type_id=1) == DEFAULT_TILE_TYPE_NAMES[1]
    assert tile_types_fixture.get_color(type_id=1) == DEFAULT_TILE_TYPE_COLORS[1]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_overwrite_road_flag_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_road_flag(type_id=type_id, road_flag=True)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_overwrite_road_flag_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_road_flag(type_id=type_id, road_flag=True)

@pytest.mark.parametrize("road_flag", NOT_BOOL_VALUES)
def test_overwrite_road_flag_invalid_flag_type(tile_types_fixture, road_flag):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=road_flag)

# ===== overwrite road flags =====
def test_overwrite_road_flags(tile_types_fixture):
    new_road_flags = [True] * len(DEFAULT_TILE_TYPE_ROAD_FLAGS)
    tile_types_fixture.overwrite_road_flags(new_road_flags=new_road_flags)
    road_flags = tile_types_fixture.get_road_flags()
    assert len(road_flags) == len(new_road_flags)
    assert road_flags == new_road_flags

def test_overwrite_road_flags_not_affect_name_or_color(tile_types_fixture):
    new_road_flags = [True] * len(DEFAULT_TILE_TYPE_ROAD_FLAGS)
    tile_types_fixture.overwrite_road_flags(new_road_flags=new_road_flags)

    for type_id in range(len(new_road_flags)):
        assert tile_types_fixture.get_road_flag(type_id=type_id) == True
        assert tile_types_fixture.get_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]
        assert tile_types_fixture.get_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]

@pytest.mark.parametrize("new_road_flags", NOT_LIST_VALUES)
def test_overwrite_road_flags_invalid_type(tile_types_fixture, new_road_flags):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_road_flags(new_road_flags=new_road_flags)

@pytest.mark.parametrize("new_road_flags", [
    [True, False],  # too short
    [True] * 16 + [False],  # too long
])
def test_overwrite_road_flags_invalid_length(tile_types_fixture, new_road_flags):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_road_flags(new_road_flags=new_road_flags)

def test_overwrite_road_flags_invalid_type_in_list(tile_types_fixture):
    new_road_flags = [True, False, True, False] + [123] * 12
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_road_flags(new_road_flags=new_road_flags)

# ===== overwrite road flags dict =====
def test_overwrite_road_flags_dict(tile_types_fixture):
    new_road_flags_dict = {
        0: True,
        1: False,
        2: True,
        3: False,
        10: True
    }
    tile_types_fixture.overwrite_road_flags_dict(new_road_flags_dict=new_road_flags_dict)
    for type_id, can_have_road in new_road_flags_dict.items():
        assert tile_types_fixture.get_road_flag(type_id=type_id) == can_have_road

def test_overwrite_road_flags_dict_not_affect_other_flags(tile_types_fixture):
    new_road_flags_dict = {
        0: True,
        1: False,
        2: True,
        3: False,
        10: True
    }
    tile_types_fixture.overwrite_road_flags_dict(new_road_flags_dict=new_road_flags_dict)

    for type_id in range(len(DEFAULT_TILE_TYPE_ROAD_FLAGS)):
        if type_id in new_road_flags_dict:
            assert tile_types_fixture.get_road_flag(type_id=type_id) == new_road_flags_dict[type_id]
        else:
            assert tile_types_fixture.get_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

def test_overwrite_road_flags_dict_not_affect_name_or_color(tile_types_fixture):
    new_road_flags_dict = {
        0: True,
        1: False,
        2: True,
        3: False,
        10: True
    }
    tile_types_fixture.overwrite_road_flags_dict(new_road_flags_dict=new_road_flags_dict)

    for type_id in range(len(DEFAULT_TILE_TYPE_ROAD_FLAGS)):
        assert tile_types_fixture.get_name(type_id=type_id) == DEFAULT_TILE_TYPE_NAMES[type_id]
        assert tile_types_fixture.get_color(type_id=type_id) == DEFAULT_TILE_TYPE_COLORS[type_id]

@pytest.mark.parametrize("new_road_flags_dict", NOT_DICT_VALUES)
def test_overwrite_road_flags_dict_invalid_type(tile_types_fixture, new_road_flags_dict):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_road_flags_dict(new_road_flags_dict=new_road_flags_dict)

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_overwrite_road_flags_dict_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.overwrite_road_flags_dict(new_road_flags_dict={type_id: True})

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_overwrite_road_flags_dict_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_road_flags_dict(new_road_flags_dict={type_id: True})

@pytest.mark.parametrize("can_have_road", NOT_BOOL_VALUES)
def test_overwrite_road_flags_dict_invalid_flag_type(tile_types_fixture, can_have_road):
    with pytest.raises(TypeError):
        tile_types_fixture.overwrite_road_flags_dict(new_road_flags_dict={0: can_have_road})

# ===== get default road flag =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_get_default_road_flag(tile_types_fixture, type_id):
    assert tile_types_fixture.get_default_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_get_default_road_flag_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.get_default_road_flag(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_get_default_road_flag_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.get_default_road_flag(type_id=type_id)

# ===== get default road flags =====
def test_get_default_road_flags(tile_types_fixture):
    default_road_flags = tile_types_fixture.get_default_road_flags()
    assert len(default_road_flags) == len(DEFAULT_TILE_TYPE_ROAD_FLAGS)
    assert default_road_flags == DEFAULT_TILE_TYPE_ROAD_FLAGS

# ===== to default road flag =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_to_default_road_flag(tile_types_fixture, type_id):
    tile_types_fixture.overwrite_road_flag(type_id=type_id, road_flag=not DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id])

    tile_types_fixture.to_default_road_flag(type_id=type_id)

    assert tile_types_fixture.get_road_flag(type_id=type_id) == DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]

def test_to_default_road_flag_not_affect_other_flags(tile_types_fixture):
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)
    tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=True)

    tile_types_fixture.to_default_road_flag(type_id=0)

    assert tile_types_fixture.get_road_flag(type_id=0) == DEFAULT_TILE_TYPE_ROAD_FLAGS[0]
    assert tile_types_fixture.get_road_flag(type_id=1) == True

def test_to_default_road_flag_not_affect_name_or_color(tile_types_fixture):
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")

    tile_types_fixture.to_default_road_flag(type_id=0)

    assert tile_types_fixture.get_road_flag(type_id=0) == DEFAULT_TILE_TYPE_ROAD_FLAGS[0]
    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_color(type_id=0) == "#123456"

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_to_default_road_flag_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.to_default_road_flag(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_to_default_road_flag_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.to_default_road_flag(type_id=type_id)

# ===== to default road flags =====
def test_to_default_road_flags(tile_types_fixture):
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)
    tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=True)

    tile_types_fixture.to_default_road_flags()

    assert tile_types_fixture.get_road_flag(type_id=0) == DEFAULT_TILE_TYPE_ROAD_FLAGS[0]
    assert tile_types_fixture.get_road_flag(type_id=1) == DEFAULT_TILE_TYPE_ROAD_FLAGS[1]

def test_to_default_road_flags_not_affect_name_or_color(tile_types_fixture):
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)
    tile_types_fixture.overwrite_road_flag(type_id=1, road_flag=True)
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#123456")

    tile_types_fixture.to_default_road_flags()

    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_color(type_id=1) == "#123456"

"""========================
        IDs
========================"""

# ===== get id from name ======
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_get_id_from_name(tile_types_fixture, type_id):
    assert tile_types_fixture.get_id_from_name(name=DEFAULT_TILE_TYPE_NAMES[type_id]) == type_id

@pytest.mark.parametrize("name", NOT_STR_VALUES)
def test_get_id_from_name_invalid_type(tile_types_fixture, name):
    with pytest.raises(TypeError):
        tile_types_fixture.get_id_from_name(name=name)

# ===== validate index =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_validate_id(tile_types_fixture, type_id):
    assert tile_types_fixture.validate_id(type_id=type_id) == True

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_validate_id_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.validate_id(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_validate_id_invalid_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.validate_id(type_id=type_id)

# ===== in range index =====
@pytest.mark.parametrize("type_id", VALID_ID_VALUES)
def test_in_range_id(tile_types_fixture, type_id):
    assert tile_types_fixture.in_range_id(type_id=type_id) == True

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_in_range_id_outside(tile_types_fixture, type_id):
    assert tile_types_fixture.in_range_id(type_id=type_id) == False

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_in_range_id_invalid_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.in_range_id(type_id=type_id)

"""================================
    Whole tile type management
================================"""

# ===== to defaults =====
def test_to_defaults(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#123456")
    tile_types_fixture.overwrite_road_flag(type_id=8, road_flag=False)

    tile_types_fixture.to_defaults()

    assert tile_types_fixture.get_name(type_id=0) == DEFAULT_TILE_TYPE_NAMES[0]
    assert tile_types_fixture.get_color(type_id=1) == DEFAULT_TILE_TYPE_COLORS[1]
    assert tile_types_fixture.get_road_flag(type_id=8) == DEFAULT_TILE_TYPE_ROAD_FLAGS[8]

# ===== to default/clear =====
def test_to_default(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)

    tile_types_fixture.to_default(type_id=0)

    assert tile_types_fixture.get_name(type_id=0) == DEFAULT_TILE_TYPE_NAMES[0]
    assert tile_types_fixture.get_color(type_id=0) == DEFAULT_TILE_TYPE_COLORS[0]
    assert tile_types_fixture.get_road_flag(type_id=0) == DEFAULT_TILE_TYPE_ROAD_FLAGS[0]

def test_to_default_not_affect_other_types(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=0, new_color="#123456")
    tile_types_fixture.overwrite_road_flag(type_id=0, road_flag=False)

    tile_types_fixture.overwrite_name(type_id=1, new_name="New Water")

    tile_types_fixture.to_default(type_id=1)

    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_color(type_id=0) == "#123456"
    assert tile_types_fixture.get_road_flag(type_id=0) == False

    assert tile_types_fixture.get_name(type_id=1) == "Water"

@pytest.mark.parametrize("type_id", INVALID_ID_VALUES)
def test_to_default_invalid_id_value(tile_types_fixture, type_id):
    with pytest.raises(ValueError):
        tile_types_fixture.to_default(type_id=type_id)

@pytest.mark.parametrize("type_id", NOT_INT_VALUES)
def test_to_default_invalid_id_type(tile_types_fixture, type_id):
    with pytest.raises(TypeError):
        tile_types_fixture.to_default(type_id=type_id)

# ===== serialize =====
def test_serialize(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#123456")
    tile_types_fixture.overwrite_road_flag(type_id=8, road_flag=False)

    data = tile_types_fixture.serialize()
    assert isinstance(data, dict)
    assert "names" in data
    assert "colors" in data
    assert "road_flags" in data

    assert data["names"][0] == "New Other"
    assert data["colors"][1] == "#123456"
    assert data["road_flags"][8] == False

# ===== deserialize =====
def test_deserialize(tile_types_fixture):
    # create data to deserialize
    data = {
        "names": ["New Other"] + tile_types_fixture.get_names()[1:],
        "colors": ["#123456"] + tile_types_fixture.get_colors()[1:],
        "road_flags": [False] + tile_types_fixture.get_road_flags()[1:]
    }

    tile_types_fixture.deserialize(data)

    assert tile_types_fixture.get_name(type_id=0) == "New Other"
    assert tile_types_fixture.get_color(type_id=0) == "#123456"
    assert tile_types_fixture.get_road_flag(type_id=0) == False

@pytest.mark.parametrize("data", NOT_DICT_VALUES)
def test_deserialize_invalid_type(tile_types_fixture, data):
    with pytest.raises(TypeError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("missing_key", ["names", "colors", "road_flags"])
def test_deserialize_missing_keys(tile_types_fixture, missing_key):
    data = {
        "names": ["New Other"] + tile_types_fixture.get_names()[1:],
        "colors": tile_types_fixture.get_colors(),
        "road_flags": [False] + tile_types_fixture.get_road_flags()[1:]
    }
    data.pop(missing_key)
    with pytest.raises(ValueError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("names", [
    ["New Other"],  # too short
    ["New Other"] * 15, # too short
    ["New Other"] * 17  # too long
])
def test_deserialize_invalid_names_length(tile_types_fixture, names):
    data = {
        "names": names,
        "colors": tile_types_fixture.get_colors(),
        "road_flags": tile_types_fixture.get_road_flags()
    }
    with pytest.raises(ValueError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("colors", [
    ["#123456"],  # too short
    ["#123456"] * 15, # too short
    ["#123456"] * 17  # too long
])
def test_deserialize_invalid_colors_length(tile_types_fixture, colors):
    data = {
        "names": tile_types_fixture.get_names(),
        "colors": colors,
        "road_flags": tile_types_fixture.get_road_flags()
    }
    with pytest.raises(ValueError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("road_flags", [
    [False],  # too short
    [False] * 15, # too short
    [False] * 17  # too long
])
def test_deserialize_invalid_road_flags_length(tile_types_fixture, road_flags):
    data = {
        "names": tile_types_fixture.get_names(),
        "colors": tile_types_fixture.get_colors(),
        "road_flags": road_flags
    }
    with pytest.raises(ValueError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("not_list", NOT_LIST_VALUES)
def test_deserialize_invalid_key_type(tile_types_fixture, not_list):
    data = {
        "names": not_list,
        "colors": tile_types_fixture.get_colors(),
        "road_flags": tile_types_fixture.get_road_flags()
    }
    with pytest.raises(TypeError):
        tile_types_fixture.deserialize(data)

    data = {
        "names": tile_types_fixture.get_names(),
        "colors": not_list,
        "road_flags": tile_types_fixture.get_road_flags()
    }
    with pytest.raises(TypeError):
        tile_types_fixture.deserialize(data)

    data = {
        "names": tile_types_fixture.get_names(),
        "colors": tile_types_fixture.get_colors(),
        "road_flags": not_list
    }
    with pytest.raises(TypeError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("not_str", NOT_STR_VALUES)
def test_deserialize_invalid_type_in_lists(tile_types_fixture, not_str):
    data = {
        "names": tile_types_fixture.get_names(),
        "colors": tile_types_fixture.get_colors(),
        "road_flags": tile_types_fixture.get_road_flags()
    }
    data["names"][0] = not_str
    with pytest.raises(TypeError):
        tile_types_fixture.deserialize(data)

    data["names"][0] = "New Other"
    data["colors"][0] = not_str
    with pytest.raises(TypeError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("not_bool", NOT_BOOL_VALUES)
def test_deserialize_invalid_flag_type_in_lists(tile_types_fixture, not_bool):
    data = {
        "names": tile_types_fixture.get_names(),
        "colors": tile_types_fixture.get_colors(),
        "road_flags": tile_types_fixture.get_road_flags()
    }
    data["road_flags"][0] = not_bool
    with pytest.raises(TypeError):
        tile_types_fixture.deserialize(data)

@pytest.mark.parametrize("invalid_color", ["#12345", "#1234567", "123456", "#ZZZZZZ"])
def test_deserialize_invalid_color_format_in_lists(tile_types_fixture, invalid_color):
    data = {
        "names": tile_types_fixture.get_names(),
        "colors": tile_types_fixture.get_colors(),
        "road_flags": tile_types_fixture.get_road_flags()
    }
    data["colors"][0] = invalid_color
    with pytest.raises(ValueError):
        tile_types_fixture.deserialize(data)

# ===== copy instance =====
def test_copy(tile_types_fixture):
    tile_types_fixture.overwrite_name(type_id=0, new_name="New Other")
    tile_types_fixture.overwrite_color(type_id=1, new_color="#123456")
    tile_types_fixture.overwrite_road_flag(type_id=8, road_flag=False)

    copy_instance = tile_types_fixture.copy()

    assert copy_instance.get_name(type_id=0) == "New Other"
    assert copy_instance.get_color(type_id=1) == "#123456"
    assert copy_instance.get_road_flag(type_id=8) == False

    tile_types_fixture.overwrite_name(type_id=0, new_name="Modified Other")
    assert copy_instance.get_name(type_id=0) == "New Other"
