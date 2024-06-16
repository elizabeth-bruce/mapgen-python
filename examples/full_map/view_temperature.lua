function temperature (x, y)
  blue = {55,169,225}
  red = {225,55,55}
  temperature = get_tile(x, y).temperature

  r = blue[1] + math.floor((red[1] - blue[1]) * ((300 - temperature)/(50)))
  g = blue[2] - math.floor((blue[2] - red[2]) * ((300 - temperature)/(50)))
  b = blue[3] - math.floor((blue[3] - red[3]) * ((300 - temperature)/(50)))

  return '\x1b[38;2;' .. r .. ';' .. g .. ';' .. b .. 'm█\x1b[0m'
end

