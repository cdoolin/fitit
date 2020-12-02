fitit.py
========

An upgrade to scipy's `optimize.curve_fit` function.  Replaces passing
parameters as arrays with passing a Params object to allow such things as
easily disabling a fit parameter.  Also provides support for simultaneus fits.

Documentation to come...


## Install

```sh
pip install git+https://github.com/cdoolin/fitit@master
```

## Usage

```python

# Params class stores the fit variables and allows attribute access
p0_peak = fitit.Params('A k f0_opt y0')

# function to fit, accepts Params as second argument
def peak(f, p):
    df = f - p.f0_opt
    return p.A / (p.k**2 / 4. + df**2.) + p.y0


# create a copy of p0_peak and set initial fit parameters
p0 = fitit.Params(like=p0_peak)
p0.f0_opt = 195047
p0.k = 60
p0.A = 4e10 * p0.k**2 / 4.

# do the fit, returns another Params object
popt = fitit.fit(peak, fopt, Pzz, p0, sigma=1)


figure()

plot(fopt, Pzz, 'o')

plot(fopt, peak(fopt, p0))
plot(fopt, peak(fopt, popt))
```
