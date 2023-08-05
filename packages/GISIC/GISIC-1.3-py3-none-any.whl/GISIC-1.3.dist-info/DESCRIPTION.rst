Gaussian Inflection Spline Interpolation Continuum (GISIC)

Author: Devin D. Whitten

Date: February 18, 2018

This package performs normalization of astronomical spectra based on a continuum identification routine.
GISIC performs a gaussian smoothing of the flux array, and identifies molecular bands based on a numerical gradient. Continuum points are then interpolated with a cubic spline.

```python
import GISIC
wave, norm_flux, continuum = GISIC.normalize(wave, flux, sigma=30)
```



