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

    r = black[1] + math.floor((blue[1] - black[1]) * (precipitation/2000))
    g = black[2] + math.floor((blue[2] - black[2]) * (precipitation/2000))
    b = black[3] + math.floor((blue[3] - black[3]) * (precipitation/2000))

    return render_character(r, g, b)
end

function temperature (x, y)
    blue = {55,169,225}
    red = {225,55,55}
    temperature = get_tile(x, y).temperature

    r = blue[1] + math.floor((red[1] - blue[1]) * ((303 - temperature)/(100)))
    g = blue[2] - math.floor((blue[2] - red[2]) * ((303 - temperature)/(100)))
    b = blue[3] - math.floor((blue[3] - red[3]) * ((303 - temperature)/(100)))

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
