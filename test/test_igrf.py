"""
Test IGRF field
"""
import os
import pytest
import numpy as np
import numpy.testing as npt
import pandas as pd
from pathlib import Path
from datetime import datetime

from ppigrf import igrf
from ppigrf.ppigrf import yearfrac_to_datetime, shc_fn, shc_fn_igrf13, shc_fn_igrf14

# Define paths to test directory and test data directory
TEST_DIR = Path(os.path.dirname(__file__))
TEST_DATA_DIR = TEST_DIR / "data"


def load_precomputed_igrf(directory):
    """
    Loads the precomputed IGRF files from a given directory

    Parameters
    ----------
    directory : :class:`pathlib.Path`

    Returns
    -------
    igrf_precomputed : :class:`pandas.Dataframe`
        Dataframe containing the precomputed values of the IGRF on the given
        date.
    """
    # Read the csv files
    first_columns = ["date", "latitude", "longitude", "altitude_km"]
    components = ("b_e", "b_n", "b_z")
    dataframes = []
    for component in components:
        columns = first_columns + [component, component + "_sv"]
        fname = directory / f"{component}.csv"
        df = pd.read_csv(fname, skiprows=13, names=columns)
        dataframes.append(df)
    # Merge the dataframes
    igrf_precomputed = pd.merge(dataframes[0], dataframes[1])
    igrf_precomputed = pd.merge(igrf_precomputed, dataframes[-1])
    # Convert the data in the dataframe into a datetime object
    decimal_date = igrf_precomputed.date.values[0]
    (date,) = yearfrac_to_datetime([decimal_date])
    igrf_precomputed = igrf_precomputed.assign(date=date)
    return igrf_precomputed


class TestIGRFKnownValues:
    """
    Test the IGRF field against precomputed values
    """

    rtol = 1e-2  # 1% of error

    @pytest.mark.parametrize(
        "date, subdirectory, igrf_version, atol",
        [
            [datetime(2010, 1, 1), "dgrf-2010-01-01", shc_fn_igrf13, 1],
            [datetime(2010, 1, 1), "dgrf-2010-01-01", shc_fn_igrf14, 1],
            [datetime(2020, 1, 1), "igrf13-2020-01-01", shc_fn_igrf13, 1],
            [datetime(2022, 10, 5), "igrf13-2022-10-05", shc_fn_igrf13, 4],
        ],
        ids=[
            "IGRF-13: dgrf-2010-01-01",
            "IGRF-14: dgrf-2010-01-01",
            "IGRF-13: igrf13-2020-01-01",
            "IGRF-13: igrf13-2022-10-05",
        ],
    )
    def test_igrf(self, date, subdirectory, igrf_version, atol):
        """
        Test IGRF against the precomputed values

        The test on 2020-01-01 doesn't involve any interpolation on the
        dates. The atol (in nT) has been chosen for each case to account points
        where the component is close to zero. For the second date that involves
        an interpolation in time the atol has been increased to account for
        differences due to different types of dates interpolations.
        """
        # Get precomputed IGRF field
        precomputed_igrf = load_precomputed_igrf(TEST_DATA_DIR/subdirectory)
        # Overwrite the date with the one in the data file
        # date = precomputed_igrf.date.values[0]
        # Compute igrf using ppigrf
        b_e, b_n, b_u = igrf(
            precomputed_igrf.longitude,
            precomputed_igrf.latitude,
            precomputed_igrf.altitude_km,
            date,
            coeff_fn=igrf_version,
        )
        # Ravel the arrays
        b_e, b_n, b_u = tuple(np.ravel(component) for component in (b_e, b_n, b_u))
        # Check if the values are equal to the expected ones
        npt.assert_allclose(b_e, precomputed_igrf.b_e, rtol=self.rtol, atol=atol)
        npt.assert_allclose(b_n, precomputed_igrf.b_n, rtol=self.rtol, atol=atol)
        npt.assert_allclose(
            b_u, -precomputed_igrf.b_z, rtol=self.rtol, atol=atol
        )  # invert the direction of b_z
