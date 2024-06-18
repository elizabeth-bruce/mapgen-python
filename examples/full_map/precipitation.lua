---The below functions use a very basic model for calculating precipitation on a per-tile basis:
---T_I + E = T_O + P
---T_I| Transfer_In  | The amount of atmospheric moisture transfered from the tile to the left (x-1)
---  E| Evaporation  | The amount of atmospheric moisture evaporated from the tile
---T_O| Transfer_Out | The amount of atmospheric moisture transfered to the tile to the left (x + 1)
---  P| Precipitation| The amount of atmopsheric moisture precipitated onto the tile
---
---All amounts are in average precipitation, mm/year, and assume a W->E wind pattern across the entire map.
---In addition to this, we model two very basic ideas:
---Evaporation increases in areas with increased temperature
---Precipitation increases in areas with high mountains (rain shadow effect)

---@param x number
---@param y number
---@return number precipitation Annual average air moisture in tile from transfer and evaporation, in mm.
function precipitation_available(x, y)
    transfer_in = 0
    if x > 0 then
        transfer_in = get_tile(x - 1, y).precipitation_available
    end

    tile = get_tile(x, y)
    height = tile.height
    latitude = tile.latitude

    EVAPORATION_CONSTANT = 1500
    LATITUDE_FACTOR = ((70 - latitude) * 30)

    evaporation = (height <= 0) and (EVAPORATION_CONSTANT + LATITUDE_FACTOR) or 0

    precipitation_available = evaporation + transfer_in

    return precipitation_available
end

---@param x number
---@param y number
---@return number precipitation Annual average non-precipitated air moisture available for transfer in the tile, in mm.
function precipitation_transfer(x, y)
    tile = get_tile(x, y)
    precipitation_available = tile.precipitation_available
    height = tile.height
    latitude = tile.latitude

    PRECIPITATION_CONSTANT = 1000
    HEIGHT_FACTOR = (math.max(height, 0)) / 10
    LATITUDE_FACTOR = ((70 - latitude) * 30)

    precipitation = math.min(precipitation_available, PRECIPITATION_CONSTANT + LATITUDE_FACTOR + HEIGHT_FACTOR)

    return precipitation_available - precipitation

end

---@param x number
---@param y number
---@return number precipitation Annual average precipitation for the tile, in mm.
function precipitation(x, y)
    tile = get_tile(x, y)
    precipitation_available = tile.precipitation_available
    height = tile.height
    latitude = tile.latitude

    PRECIPITATION_CONSTANT = 1000
    HEIGHT_FACTOR = (math.max(height, 0)) / 10
    LATITUDE_FACTOR = ((70 - latitude) * 30)

    precipitation = math.min(precipitation_available, PRECIPITATION_CONSTANT + LATITUDE_FACTOR + HEIGHT_FACTOR)

    return precipitation
end
