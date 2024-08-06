import json
import os
import pytest

from mapgen.data.errors import UnknownLayerGeneratorException, InvalidContextException
from mapgen.data.models import LayerConfiguration


def test_validate_layer_configuration_unknown_generator():
    with pytest.raises(UnknownLayerGeneratorException) as exc:
        LayerConfiguration(
            'test_layer',
            'unknown_generator',
            {
                "type": "int"
            }
        )

def test_validate_layer_configuration_bad_context():
    with pytest.raises(InvalidContextException) as exc:
        LayerConfiguration(
            'test_layer',
            'FREQUENCY_FILTERED_NOISE',
            {
               'foo': 'bar'
            } 
        )
