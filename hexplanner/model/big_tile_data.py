from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class BigTileData:
    tile_type_id: int
    has_road: bool
    height: int
    x: int
    y: int

    def __post_init__(self) -> None:
        if not isinstance(self.tile_type_id, int) or isinstance(self.tile_type_id, bool):
            raise TypeError("tile_type_id must be an integer")
        if self.tile_type_id < 0 or self.tile_type_id > 15:
            raise ValueError("tile_type_id must be in range 0..15")

        if not isinstance(self.has_road, bool):
            raise TypeError("has_road must be a boolean")

        if not isinstance(self.height, int) or isinstance(self.height, bool):
            raise TypeError("height must be an integer")
        if self.height < 0 or self.height > 255:
            raise ValueError("height must be in range 0..255")

        if not isinstance(self.x, int) or isinstance(self.x, bool):
            raise TypeError("x must be an integer")
        if not isinstance(self.y, int) or isinstance(self.y, bool):
            raise TypeError("y must be an integer")
