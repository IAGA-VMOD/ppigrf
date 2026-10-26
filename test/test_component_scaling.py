"""Compute directions without squaring components in their input dtype."""

import numpy as np
import numpy.testing as npt
import pytest

from ppigrf import get_inclination_declination


@pytest.mark.parametrize(
    "dtype, scale", [(np.int32, 1), (np.float32, 1e20), (np.float32, 1e-30)]
)
def test_horizontal_magnitude_without_overflow(dtype, scale):
    components = [
        np.array([value * scale], dtype=dtype) for value in (30000.0, 40000.0, -50000.0)
    ]
    inclination, declination = get_inclination_declination(*components)
    npt.assert_allclose(inclination, [45.0], rtol=2e-7)
    npt.assert_allclose(declination, [36.86989764584402], rtol=2e-7)
