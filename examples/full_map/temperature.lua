---@param x number
---@param y number
---@return number temp Average annual temperature of the tile, in K
function temperature(x, y)
    tile = get_tile(x, y)

    height = tile.height
    latitude = tile.latitude

    base_temperature = 303

    latitude_factor = 0.45 * latitude
    height_factor = 0.25 * math.sqrt(math.max(height, 0))

    temperature = base_temperature - height_factor - latitude_factor

    return temperature
end
