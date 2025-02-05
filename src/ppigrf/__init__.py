from __future__ import annotations

from ._version import version as __version__
from .ppigrf import get_inclination_declination, igrf, igrf_gc

__all__ = ["__version__", "get_inclination_declination", "igrf", "igrf_gc"]
