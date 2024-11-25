# Data files used for testing ppigrf

## Precomputed IGRF

Each one of these folders contain a set of `b_e.csv`, `b_n.csv` and `b_z.csv`
files that host precomputed values of the IGRF field obtained through the [NCEI
Geomagnetic
Calculator](https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml)
provided by [NOAA](https://www.ngdc.noaa.gov).

These values were computed in a regular grid with a spacing of 1 degree in both
longitudinal and latitudinal directions, at a height of 5km above the WGS84
ellipsoid. The date of each IGRF field files is specified in the folder name
following the `YYYY-MM-DD` format.

The `b_z.csv` contains the **downward** components of the magnetic vector on
each location.

Note that each IGRF release includes the DGRF (definitive field) for the previous epoch. IGRF-14 includes the DGRF for 2020.0, overriding the IGRF for 2020.0 issued within IGRF-13. This means that moving from IGRF-13 to IGRF-14 changes the results for calculations within the 2015-2025 period. Calculations within the definitive period (i.e. for IGRF-14 and lower: up to 2015.0) should remain the same.

```
Example requests

dgrf-2010-01-01/b_n.csv:
https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfgrid?browserRequest=true&key=gFE5W&lat1=80&lat1Hemisphere=S&lat2=80&lat2Hemisphere=N&latStepSize=1.0&lon1=179&lon1Hemisphere=W&lon2=180&lon2Hemisphere=E&lonStepSize=1.0&coordinateSystem=D&elevation=5&elevationUnits=K&magneticComponent=x&model=IGRF&startYear=2010&startMonth=01&startDay=1&endYear=2010&endMonth=1&endDay=1&dateStepSize=1.0&resultFormat=csv

dgrf-2010-01-01/b_e.csv:
https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfgrid?browserRequest=true&key=gFE5W&lat1=80&lat1Hemisphere=S&lat2=80&lat2Hemisphere=N&latStepSize=1.0&lon1=179&lon1Hemisphere=W&lon2=180&lon2Hemisphere=E&lonStepSize=1.0&coordinateSystem=D&elevation=5&elevationUnits=K&magneticComponent=y&model=IGRF&startYear=2010&startMonth=01&startDay=1&endYear=2010&endMonth=1&endDay=1&dateStepSize=1.0&resultFormat=csv

dgrf-2010-01-01/b_z.csv:
https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfgrid?browserRequest=true&key=gFE5W&lat1=80&lat1Hemisphere=S&lat2=80&lat2Hemisphere=N&latStepSize=1.0&lon1=179&lon1Hemisphere=W&lon2=180&lon2Hemisphere=E&lonStepSize=1.0&coordinateSystem=D&elevation=5&elevationUnits=K&magneticComponent=z&model=IGRF&startYear=2010&startMonth=01&startDay=1&endYear=2010&endMonth=1&endDay=1&dateStepSize=1.0&resultFormat=csv
```