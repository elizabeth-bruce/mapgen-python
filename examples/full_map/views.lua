function render_character(r, g, b, char)
    r = r or 255
    g = g or 255
    b = b or 255
    char = char or '█'
    return '\x1b[38;2;' .. r .. ';' .. g .. ';' .. b .. 'm' .. char .. '\x1b[0m'
end

function precipitation (x, y)
    black = {0,0,0}
    blue = {0,0,200}
    precipitation = get_tile(x, y).precipitation

    r = black[1] + math.floor((blue[1] - black[1]) * (precipitation/3500))
    g = black[2] + math.floor((blue[2] - black[2]) * (precipitation/3500))
    b = black[3] + math.floor((blue[3] - black[3]) * (precipitation/3500))

    return render_character(r, g, b)
end

function temperature (x, y)
    blue = {0,0,255}
    red = {255, 120, 120}
    temperature = get_tile(x, y).temperature

    r = red[1] + math.floor((blue[1] - red[1]) * ((303 - temperature)/(100)))
    g = red[2] - math.floor((red[2] - blue[2]) * ((303 - temperature)/(100)))
    b = red[3] - math.floor((red[3] - blue[3]) * ((303 - temperature)/(100)))

    return render_character(r, g, b)
end

function height(x, y)
    height = math.max(get_tile(x, y).height, 0)

    black = {0,0,0}
    silver = {230,230,230}

    r = black[1] + math.floor((silver[1] - black[1]) * (height/15000))
    g = black[2] + math.floor((silver[2] - black[2]) * (height/15000))
    b = black[3] + math.floor((silver[3] - black[3]) * (height/15000))

    return render_character(r, g, b)
end

function biotype(x, y)
    height = get_tile(x, y).height
    precipitation = get_tile(x, y).precipitation
    temperature = get_tile(x, y).temperature

    if height <= -500 then -- Oceans
        return '\x1b[38;2;0;0;255m~\x1b[0m'
    end

    if height <= 0 then -- Shallows
        return '\x1b[38;2;120;120;255m~\x1b[0m'
    end

    if height >= 15000 then -- Peaks
	return '\x1b[38;2;225;225;225m▲\x1b[0m'
    end

    if height >= 5000 then -- Mountains
        return '\x1b[38;2;175;85;85m▲\x1b[0m'
    end

    if height >= 2000 then -- Hills
	if precipitation >= 2000 then
            return '\x1b[38;2;0;255;0m∩\x1b[0m'
	end
	if precipitation < 500 then
            return '\x1b[38;2;225;190;45m∩\x1b[0m'
	end
	return '\x1b[38;2;195;205;100m∩\x1b[0m'
    end

    if precipitation < 500 then
        return '\x1b[38;2;225;190;45m.\x1b[0m'
    end

    if precipitation < 2000 then
        return '\x1b[38;2;195;205;100m.\x1b[0m'
    end 
    -- Plains
    return '\x1b[38;2;0;255;0m.\x1b[0m'
end
