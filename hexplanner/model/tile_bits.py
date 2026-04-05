TYPE_MASK   = 0b00001111
ROAD_MASK   = 0b00010000

# TYPE_BITS = 4
TYPE_MAX = 0b1111

def get_type(meta: int) -> int:
    return meta & TYPE_MASK

def set_type(meta: int, tile_type: int) -> int:
    if not isinstance(tile_type, int):
        raise TypeError("Tile type must be an integer")
    if tile_type < 0 or tile_type > TYPE_MAX:
        raise ValueError("Invalid tile type")
    meta = meta & ~TYPE_MASK
    type_bits = tile_type & TYPE_MASK
    meta = meta | type_bits
    return meta

def clear_type(meta: int) -> int:
    return meta & ~TYPE_MASK


def has_road(meta: int) -> bool:
    return (meta & ROAD_MASK) != 0

def set_road(meta: int, has_road: bool) -> int:
    if not isinstance(has_road, bool):
        raise TypeError("Road value must be a boolean")
    if has_road:
        meta = meta | ROAD_MASK
    else:
        meta = meta & ~ROAD_MASK
    return meta

def toggle_road(meta: int) -> int:
    return meta ^ ROAD_MASK

def clear_road(meta: int) -> int:
    return meta & ~ROAD_MASK


def clear_all(meta: int) -> int:
    return 0

def pack(tile_type: int, has_road: bool) -> int:
    meta = 0
    meta = set_type(meta, tile_type)
    meta = set_road(meta, has_road)
    return meta

def unpack(meta: int) -> tuple[int, bool]:
    tile_type = get_type(meta)
    has_road_value = has_road(meta)
    return tile_type, has_road_value
