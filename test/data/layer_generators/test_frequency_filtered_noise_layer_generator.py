import json
import os
import pytest

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.frequency_filtered_noise_layer_generator import FrequencyFilteredNoiseLayerGenerator

@pytest.fixture
def test_layer_configuration():
    return LayerConfiguration(
        'frequency_layer',
        'FREQUENCY_FILTERED_NOISE',
        {
            "roughness": 0.15,
            "decay_x": 2.5,
            "decay_y": 2.5,
            "decay_x_y": 0.5
        }
   )

@pytest.fixture
def test_layer_generator():
    return FrequencyFilteredNoiseLayerGenerator()

@pytest.fixture
def test_map_context():
    return MapContext("")

def test_frequency_filtered_noise_layer_generator_resolve(test_layer_configuration, test_map_context, test_layer_generator):
    layer = test_layer_generator.resolve(test_layer_configuration, test_map_context)

    assert layer.name == test_layer_configuration.name
    assert layer.type == "float"

    assert layer.roughness == test_layer_configuration.context['roughness']
    assert layer.decay_x == test_layer_configuration.context['decay_x']
    assert layer.decay_y == test_layer_configuration.context['decay_y']
    assert layer.decay_x_y == test_layer_configuration.context['decay_x_y']
