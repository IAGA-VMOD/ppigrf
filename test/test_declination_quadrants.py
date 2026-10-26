"""Check azimuth quadrants and the zero-horizontal-field convention."""

import numpy as np
import numpy.testing as npt
import pytest

from ppigrf import get_inclination_declination


@pytest.mark.parametrize("degrees", (True, False))
def test_declination_all_quadrants(degrees):
    east = np.array([1.0, -1.0, 0.0, 1.0, -1.0, 0.0, 0.0])
    north = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 0.0])
    expected = np.array([135.0, -135.0, 180.0, 45.0, -45.0, 0.0, 0.0])
    if not degrees:
        expected = np.radians(expected)
    _, declination = get_inclination_declination(
        east, north, np.zeros_like(east), degrees=degrees
    )
    npt.assert_allclose(declination, expected, atol=1e-14)
