## mapgen
------
mapgen is a tile-based, 2D map generation tool to procedurally generate maps for  fantasy worldbuilding, tabletop campaign settings, and other similar cases. It aims to be both highly customizable for the user and easy-to-use - to do this, the user writes Lua code to detail individual properties of the world, which mapgen then uses to create a map that satisfies these properies.

Once created, maps can be either exported to a NumPy file, or viewed in-console using user-defined views, again written in Lua, that specify how to display the map.

### Example
-------
To generate and view a map:

```sh
poetry install
cd examples/full_map
# Creates the map specified in the directory and saves to map.npz
poetry run mapgen create
# Loads the map from map.npz and renders the height property in-console
poetry run mapgen view height
```

### Creating a Map
--------

Each map is composed of a 2D square grid of _tiles_ - tiles, in turn, are each composed of a number of _layers_, each of which specify an individual property of the tile. Maps are defined in a special JSON file called a _map configuration file_, with the following format:

```json
{
    "name": <str>,
    "width": <int>,
    "height": <int>,
    "layer_configurations": [{
        "name": <str>,
        "generator": <"FREQUENCY_FILTERED_NOISE"|"LUA">,
        "context": {
            <generator-specific content>
        }
    }, ...]
}

```

An full example of this format can be found in the `examples/full_map` directory.

#### Layers
Layers can be specified in a number of different ways:
* Through custom Lua code, which specifies how to calculate a layer value on a per-tile basis.
* Through a pre-set algorithm that approximates common worldbuilding algorithms.

##### Lua Layer
The custom Lua code used to calculate a layer value is written by the map author, and called a _resolver_. A resolver has the following signature in Lua:

```lua
function property_name(x, y)
    ---x is the horizontal coordinate of the tile,
    ---y is the vertical coordinate of the tile
    return x + y -- this property for the tile at (x, y) will be the number x + y
end
```

Resolvers can access the properties of other tiles on the map through the global function `get_tile`:

```lua
function sum_of_x_coordinates(x, y)
    if x == 0 then
        return 0
    end

    previous_tile = get_tile(x-1, y)

    previous_sum_of_x_coordinates = previous_tile.sum_of_x_coordinates

    return previous_sum_of_of_x_coordinates + x
end
```

Resolvers may return one of three types of Lua values: `number`, `boolean` or `string`. Any other values will result in an error on runtime.

Since resolvers for tile properties can depend on other tile properties, it is possible to introduce a circular dependency among tiles. In this case, attempting to generate a map will cause a `CircularDependencyError` at runtime:

```lua
--- Will cause a runtime error
function property_a(x, y)
    return get_tile(x, y).property_b + 1
end

function property_b(x, y)
    return get_tile(x, y).property_a + 1
end
```

Lua resolvers can be associated with a specific map property via a layer configuration setting in the map configuration file:

```json
{
    # The map will have a property called 'example',
    # which will be calculated via the function called 'example'
    # in the filename specified below
    "name": "example",
    "context": {
        "type": "float",  # Value of property, of either str, bool, float, int
        "filename": "example.lua" # Where to search for the Lua resolver
        }
    }
}
```

#### Pregenerated Layer

For convenience, mapgen also ships with an alternative method for generating properties, intended for generating height maps - this method uses an exponential low-pass filter on normally-distributed noise to generate height maps approximating continental distributions.

The exact smoothness of this distribution, along with other features, can be configured via a layer configuration setting in the map configuration file:

```json
{
    "name": "height",
    "generator": "FREQUENCY_FILTERED_NOISE",
    "context": {
        "roughness": 20, # Controls amplitude of entire height map
        "decay_x": 3.0,  # Controls how rough or smooth the height map is in the x-axis - higher value means less noise
        "decay_y": 3.0,  # Controls how rough or smooth the height map is in the y-axis - higher value means less noise
        "decay_x_y": 0.5 # Controls how rough or smooth the height map is across the entire map - higher value means less noise
    }
},
```

Once the map configuration and any Lua files needed are specified, the map can be created via `mapgen create`:

```sh
poetry run mapgen create
```

This will generate the map and save a copy of the map to `map.npz` by default (specified by `--out_file`.)


### Viewing the Map
Similar to map creation, map viewing is customized by a combination of Lua code and configuration. Maps are displayed according to a specific Lua function called a _view_, very similar to a _resolver_ used during map creation, with the same access to `get_tile`:

```lua
---For a tile specified by its x and y coordinates,
---returns a single Unicode character that will be displayed for the tile,
---'^' if set, and '_' if not.
function example_view(x, y)
    tile = get_tile(x, y)

    example_property = tile.example_property
    return (example_property and '^' or '_')
end
```

These view functions are then made accessible via a _view configuration file_, again similar to a map configuration file:

```json
{
    "views": [{
        # Creates a new view called "example_view",
        # which will use the example_view function in the specified file
        # below to render the map to the console.
        "name": "example_view",
        "type": "CONSOLE",
        "context": {
            "filename": "example_view.lua"
        }
    }]
}
```

Once this file is set, the map can now be displayed in console via the `mapgen view command`:

```sh
poetry run mapgen view example_view
```
