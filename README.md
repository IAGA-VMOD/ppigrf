# Pure Python International Geomagnetic Reference Field
[![DOI](https://zenodo.org/badge/352365168.svg)](https://zenodo.org/badge/latestdoi/352365168)

Pure Python code to calculate IGRF model predictions. The IGRF is a model of the Earth's main magnetic field that is updated every 5 years.

References:
- IAGA V-MOD WG and main IGRF website:  
  https://www.ncei.noaa.gov/products/international-geomagnetic-reference-field
- IGRF-13 (2020):
    - International Geomagnetic Reference Field: the 13th generation, Alken, P., Thébault, E., Beggan, C.D. et al. International Geomagnetic Reference Field: the thirteenth generation. Earth Planets Space 73, 49 (2021). doi: [10.1186/s40623-020-01288-x](https://doi.org/10.1186/s40623-020-01288-x)
    - [EPS Special issue detailing contributing models](https://www.springeropen.com/collections/igrf13)
- IGRF-14 (2025):
    - International Association of Geomagnetism and Aeronomy. (2024). IGRF-14. Zenodo. https://doi.org/10.5281/zenodo.14012302
    - (article in progress)
    - [In progress: EPS Special issue detailing contributing models](https://www.springeropen.com/collections/igrf14)
    - Evaluation code: https://github.com/IAGA-VMOD/IGRF14eval

**Note that this code now defaults to use IGRF-14**

## Install
The only dependencies are Numpy and Pandas. Install by either
```
pip install ppigrf
```
or clone the repository and run 
```
python setup.py install
```

Also, if you don't want to install a module but use the code in your project, just grap ppigrf.py and the .shc file (from src/ppigrf) and place it in your working directory. That's all. 

## Example
All the above choices should enable you to import like this:
```python
import ppigrf
```
IGRF model values depend on time and position. Time can be given as one or more datetimes. The position can be specified in either geodetic or geocentric coordinates. Example with geodetic coordinates:
```python
from datetime import datetime
lon = 5.32415  # degrees east
lat = 60.39299 # degrees north
h   = 0        # kilometers above sea level
date = datetime(2021, 3, 28)

Be, Bn, Bu = ppigrf.igrf(lon, lat, h, date) # returns east, north, up
```
Geodetic coordinates take the ellipsoidal shape of the Earth into account. The northward component returned by the igrf function is tangential to the ellipsoid, and in general not tangential to an Earth centered sphere. The upward component is perpendicular to the ellipsoid, and in general not perpendicular to the sphere. 

In some cases it is more convenient to work in geocentric coordinates, which are purely spherical. To do that, use the igrf_gc function:
```python
r     = 6500 # kilometers from center of Earht
theta = 30   # colatitude in degrees
phi   = 4    # degrees east (same as lon)

Br, Btheta, Bphi = ppigrf.igrf_gc(r, theta, phi, date) # returns radial, south, east
```

It is also possible to calculate magnetic field values on a grid. The code uses broadcasting rules for the coordinate inputs. You can also pass multiple dates. If you pass `K` time stamps, together with coordinates with a combined shape of e.g., `(L, M, N)`, the output will have shape `(K, L, M, N)`. Example:
```python
lon = np.array([20, 120, 220])
lat = np.array([[60, 60, 60], [-60, -60, -60]])
h   = 0
dates = [datetime(y, 1, 1) for y in np.arange(1960, 2021, 20)]
Be, Bn, Bu = ppigrf.igrf(lon, lat, h, dates)
```
The output will have shape `(4, 2, 3)`.

## How to test?

It is possible to run some tests that corroborates that `ppigrf` works as
expected. To do so you need to install [`pytest`](https://docs.pytest.org). You
can do so through `pip`:

```
pip install pytest
```

Then you need to clone this repository and install `ppigrf`:

```
python setup.py install
```

Finally you can test the installed version of `ppigrf` with:

```
pytest -v
```


## Why?
There are lots of Python modules that can calculate IGRF values. Most are wrappers of Fortran code, which can be tricky to compile. This version is pure Python. For most applications it is still quite fast. I also prefer the ppigrf interface over the alternatives. 

The code is also super portable: Just copy ppigrf.py and the .shc file to your project and you're done.

## Notes
The model coefficients are read from an .shc file. This is a file format that is used for certain spherical harmonic magnetic field models. See a selection of .shc model files here:
https://github.com/ESA-VirES/MagneticModel/blob/staging/eoxmagmod/eoxmagmod/data/

It should be straightforward to swap the IGRF .shc file with another model, but keep in mind that the time dependence may be implemented differently in other models. IGRF, and this code, uses linear interpolation between model updates, and changing the model file will not change the ppigrf interpolation setup. 

The code is vectorized, so it will be quite fast, but probably not as fast as compiled Fortran code. One application which may require more optimization is field line tracing: In the current implementation, the coefficients are loaded and interpolated in time for every function call, which gives a lot of unnecessary overhead.

Thanks to Juha Vierinen for the setup script, and for making ppigrf available via PyPI.

## Contact
If you find errors, please let me know! 

You don't need permission to copy or use this code, but I would be happy to know if it is useful for anyone else. 

karl.laundal at uib.no
