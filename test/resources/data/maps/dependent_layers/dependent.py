async def dependent(x: int, y: int, get_tile) -> int:
    return await get_tile(x,y).base - 1

