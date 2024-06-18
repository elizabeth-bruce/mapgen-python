---@param x number
---@param y number
---@return number latitude The average latitude of the tile, in degrees.
function latitude(x, y)
    LATITUDE_RANGE = 50
    LATITUDE_MAX = 70
    latitude = LATITUDE_MAX - ((y) * LATITUDE_RANGE / 60)

    return latitude
end
