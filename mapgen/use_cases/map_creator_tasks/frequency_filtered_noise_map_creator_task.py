from numpy import arange, copyto, ndarray, fft, ix_, power, random
from numpy.random import RandomState
from numpy.typing import NDArray

from mapgen.models import (
    FrequencyFilteredNoiseLayer,
    MapDefinition,
)
from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.map_creator_tasks.map_creator_task import MapCreatorTask

MU = 0
SIGMA = 1


class FrequencyFilteredNoiseMapCreatorTask(MapCreatorTask):
    def __init__(self, map_accessor: SharedMemoryMapAccessor):
        self.map_accessor = map_accessor

    def populate(
        self, map_definition: MapDefinition, random_state: RandomState
    ) -> None:
        pass

    def populate_layer(
        self, layer: FrequencyFilteredNoiseLayer, width: int, height: int
    ) -> None:
        decay_x = layer.decay_x
        decay_y = layer.decay_y
        decay_x_y = layer.decay_x_y
        roughness = layer.roughness
        name = layer.name

        X, Y = ix_(arange(width), arange(height))

        # Create a 2D grid of Gaussian noise and transform it to
        # the frequency domain
        noise_values = random.normal(MU, SIGMA, (height, width))
        frequency_noise_values = fft.rfft2(noise_values)

        # Apply a low-pass filter that exponentially dampens small frequencies
        filtered_frequency_noise_values = frequency_noise_values * (
            roughness / power(power(X, decay_x) + power(Y, decay_y) + 1, decay_x_y)
        )

        # When transforming the noise data from the frequency back to the time
        # domain, we have to include a scale factor of (width * height) to offset
        # the same amount it gets shrunk due to normalization
        filtered_noise_values = (
            width * height * fft.irfft2(filtered_frequency_noise_values)
        )

        # Write the filtered noise data to the shared memory for the layer
        shared_memory = self.map_accessor.get_shared_memory(name)
        destination: NDArray = ndarray(
            shape=(height, width), dtype=float, buffer=shared_memory
        )
        copyto(filtered_noise_values, destination)
