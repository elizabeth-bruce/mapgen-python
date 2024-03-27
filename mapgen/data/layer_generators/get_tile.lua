Tile = {}
Tile.mt = {}

Tile.mt.__index = function(table, key)
    return get_attribute_value(table.x, table.y, key)
end

function Tile.new(x, y)
    t = {x=x, y=y}
    setmetatable(t, Tile.mt)
end


function get_tile(x, y)
    return Tile.new{x=x, y=y}
end
