def dependent(x: int, y: int, get_tile) -> int:
    if x == 99:
        return 5
    else:
        return get_tile(x + 1, y).dependent + 1

