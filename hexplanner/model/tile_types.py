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

class TileTypes:
    def __init__(self):
        self.names = list(DEFAULT_TILE_TYPE_NAMES)
        self.colors = list(DEFAULT_TILE_TYPE_COLORS)
        self.road_flags = list(DEFAULT_TILE_TYPE_ROAD_FLAGS)


    def get_name(self, type_id: int) -> str:
        self.validate_id(type_id)

        return self.names[type_id]

    def get_names(self) -> list[str]:
        return self.names
    
    def overwrite_name(self, type_id: int, new_name: str) -> None:
        self.validate_id(type_id)

        if not isinstance(new_name, str):
            raise TypeError(f"Tile type name must be a string, got {type(new_name)}")

        self.names[type_id] = new_name
    
    def overwrite_names(self, new_names: list[str]) -> None:
        if not isinstance(new_names, list):
            raise TypeError(f"Tile type names must be a list, got {type(new_names)}")
        if len(new_names) != len(self.names):
            raise ValueError(f"Tile type names list must have length {len(self.names)}, got {len(new_names)}")
        if not all(isinstance(name, str) for name in new_names):
            raise TypeError("All tile type names must be strings")
        self.names = new_names
    
    def overwrite_names_dict(self, new_names_dict: dict[int, str]) -> None:
        if not isinstance(new_names_dict, dict):
            raise TypeError(f"Tile type names must be provided as a dictionary, got {type(new_names_dict)}")
        for type_id, new_name in new_names_dict.items():
            self.validate_id(type_id)
            if not isinstance(new_name, str):
                raise TypeError(f"Tile type name must be a string, got {type(new_name)} for type ID {type_id}")
            self.names[type_id] = new_name

    def get_default_name(self, type_id: int) -> str:
        self.validate_id(type_id)

        return DEFAULT_TILE_TYPE_NAMES[type_id]
    
    def get_default_names(self) -> tuple[str, ...]:
        return DEFAULT_TILE_TYPE_NAMES
    
    def to_default_name(self, type_id: int) -> None:
        self.validate_id(type_id)

        self.names[type_id] = DEFAULT_TILE_TYPE_NAMES[type_id]

    def to_default_names(self) -> None:
        self.names = list(DEFAULT_TILE_TYPE_NAMES)


    def get_color(self, type_id: int) -> str:
        self.validate_id(type_id)
        return self.colors[type_id]
    
    def get_colors(self) -> list[str]:
        return self.colors
    
    def overwrite_color(self, type_id: int, new_color: str) -> None:
        self.validate_id(type_id)
        self.validate_color_hex_string(new_color)
        self.colors[type_id] = new_color
    
    @staticmethod
    def validate_color_hex_string(color: str) -> bool:
        if not isinstance(color, str):
            raise TypeError(f"Color must be a string, got {type(color)}")
        if not color.startswith("#") or len(color) != 7:
            raise ValueError(f"Color must be a hex string in the format '#RRGGBB', got '{color}'")
        try:
            int(color[1:], 16)
        except ValueError:
            raise ValueError(f"Color must be a hex string in the format '#RRGGBB', got '{color}'")
        return True

    def overwrite_colors(self, new_colors: list[str]) -> None:
        if not isinstance(new_colors, list):
            raise TypeError(f"Tile type colors must be a list, got {type(new_colors)}")
        if len(new_colors) != len(self.colors):
            raise ValueError(f"Tile type colors list must have length {len(self.colors)}, got {len(new_colors)}")
        for color in new_colors:
            self.validate_color_hex_string(color)
        self.colors = new_colors
        return
    
    def overwrite_colors_dict(self, new_colors_dict: dict[int, str]) -> None:
        if not isinstance(new_colors_dict, dict):
            raise TypeError(f"Tile type colors must be provided as a dictionary, got {type(new_colors_dict)}")
        for type_id, new_color in new_colors_dict.items():
            self.validate_id(type_id)
            self.validate_color_hex_string(new_color)
            self.colors[type_id] = new_color

    def get_default_color(self, type_id: int) -> str:
        self.validate_id(type_id)
        return DEFAULT_TILE_TYPE_COLORS[type_id]
    
    def get_default_colors(self) -> list[str]:
        return DEFAULT_TILE_TYPE_COLORS
    
    def to_default_color(self, type_id: int) -> None:
        self.validate_id(type_id)
        self.colors[type_id] = DEFAULT_TILE_TYPE_COLORS[type_id]
    
    def to_default_colors(self) -> None:
        self.colors = list(DEFAULT_TILE_TYPE_COLORS)
    

    def get_road_flag(self, type_id: int) -> bool:
        self.validate_id(type_id)
        return self.road_flags[type_id]
    
    def get_road_flags(self) -> list[bool]:
        return self.road_flags
    
    def overwrite_road_flag(self, type_id: int, road_flag: bool) -> None:
        self.validate_id(type_id)
        if not isinstance(road_flag, bool):
            raise TypeError(f"Road flag must be a boolean, got {type(road_flag)}")
        self.road_flags[type_id] = road_flag
    
    def overwrite_road_flags(self, new_road_flags: list[bool]) -> None:
        if not isinstance(new_road_flags, list):
            raise TypeError(f"Tile type road flags must be a list, got {type(new_road_flags)}")
        if len(new_road_flags) != len(self.road_flags):
            raise ValueError(f"Tile type road flags list must have length {len(self.road_flags)}, got {len(new_road_flags)}")
        if not all(isinstance(flag, bool) for flag in new_road_flags):
            raise TypeError("All tile type road flags must be booleans")
        self.road_flags = new_road_flags
    
    def overwrite_road_flags_dict(self, new_road_flags_dict: dict[int, bool]) -> None:
        if not isinstance(new_road_flags_dict, dict):
            raise TypeError(f"Tile type road flags must be provided as a dictionary, got {type(new_road_flags_dict)}")
        for type_id, new_road_flag in new_road_flags_dict.items():
            self.validate_id(type_id)
            if not isinstance(new_road_flag, bool):
                raise TypeError(f"Road flag must be a boolean, got {type(new_road_flag)} for type ID {type_id}")
            self.road_flags[type_id] = new_road_flag
    
    def get_default_road_flag(self, type_id: int) -> bool:
        self.validate_id(type_id)
        return DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]
    
    def get_default_road_flags(self) -> list[bool]:
        return DEFAULT_TILE_TYPE_ROAD_FLAGS
    
    def to_default_road_flag(self, type_id: int) -> None:
        self.validate_id(type_id)
        self.road_flags[type_id] = DEFAULT_TILE_TYPE_ROAD_FLAGS[type_id]
    
    def to_default_road_flags(self) -> None:
        self.road_flags = list(DEFAULT_TILE_TYPE_ROAD_FLAGS)


    def get_id_from_name(self, name: str) -> int:
        if not isinstance(name, str):
            raise TypeError(f"Tile type name must be a string, got {type(name)}")
        try:
            return self.names.index(name)
        except ValueError:
            raise ValueError(f"Tile type name '{name}' not found")
    
    def validate_id(self, type_id: int) -> bool:
        if not isinstance(type_id, int) or isinstance(type_id, bool):
            raise TypeError(f"Tile type ID must be an integer, got {type(type_id)}")
        if not (0 <= type_id < len(self.names)):
            raise ValueError(f"Tile type ID {type_id} is out of valid range (0 to {len(self.names) - 1})")
        return True
    
    def in_range_id(self, type_id: int) -> bool:
        if not isinstance(type_id, int) or isinstance(type_id, bool):
            raise TypeError(f"Tile type ID must be an integer, got {type(type_id)}")
        return 0 <= type_id < len(self.names)
    

    def to_default(self, type_id: int) -> None:
        self.validate_id(type_id)

        self.to_default_name(type_id)
        self.to_default_color(type_id)
        self.to_default_road_flag(type_id)
    
    def to_defaults(self) -> None:
        self.to_default_names()
        self.to_default_colors()
        self.to_default_road_flags()

    def serialize(self) -> dict:
        data_dict = {
            "names": self.names,
            "colors": self.colors,
            "road_flags": self.road_flags
        }
        return data_dict
    
    def deserialize(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Data must be a dictionary, got {type(data)}")
        if "names" not in data:
            raise ValueError("Data missing 'names' key")
        if "colors" not in data:
            raise ValueError("Data missing 'colors' key")
        if "road_flags" not in data:
            raise ValueError("Data missing 'road_flags' key")

        for key in ["names", "colors", "road_flags"]:
            if not isinstance(data[key], list):
                raise TypeError(f"Data for '{key}' must be a list, got {type(data[key])}")
            if len(data[key]) != len(self.names):
                raise ValueError(f"Data list for '{key}' must have length {len(self.names)}, got {len(data[key])}")

        if not all(isinstance(name, str) for name in data["names"]):
            raise TypeError("All tile type names must be strings")
        for color in data["colors"]:
            self.validate_color_hex_string(color)
        if not all(isinstance(flag, bool) for flag in data["road_flags"]):
            raise TypeError("All tile type road flags must be booleans")

        self.names = data["names"]
        self.colors = data["colors"]
        self.road_flags = data["road_flags"]

    def copy(self) -> "TileTypes":
        new_tile_types = TileTypes()
        new_tile_types.names = self.names.copy()
        new_tile_types.colors = self.colors.copy()
        new_tile_types.road_flags = self.road_flags.copy()
        return new_tile_types
    
