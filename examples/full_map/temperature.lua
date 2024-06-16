function temperature(x, y)
    height = get_tile(x, y).height

    return 303 - math.sqrt(math.max(height, 0))
end
