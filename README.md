fitit.py
========

An interface to scipy's `optimize.curve_fit` function.  `fitit` Replaces passing
parameters as arrays with passing a Params object to allow such things as
easily disabling a fit parameter.

## Install

```sh
pip install fitit
```

## Usage

```python
import fitit

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
p0.y0 = 0

# do the fit, returns another Params object
popt = fitit.fit(peak, fopt, Pzz, p0, sigma=1)


figure()

plot(fopt, Pzz, 'o')

plot(fopt, peak(fopt, p0))
plot(fopt, peak(fopt, popt))
```

### Holding parameters constant

To hold parameters constant, and not pass the parameter to the least squares algorithm, prefix the parameter with a star:
```python
p0 = fitit.Params('A k f0_opt *y0')
```

### Bounded fit

Upper and lower bounds on the fit can also be specified:

```python
# inital guess parameters
p0 = fitit.Params('A k f0_opt *y0')
p0.f0_opt = 195047
p0.k = 60
p0.A = 4e10 * p0.k**2 / 4.
p0.y0 = 0

# lower limits
p_lower = fitit.Params(like=p0)
p_lower.f0_opt = p0.f0_opt - 100
p_lower.k = 0
p_lower.A = 0

# upper limits
p_upper = fitit.Params(like=p0)
p_upper.f0_opt = p0.f0_opt + 100
p_upper.k = 100
p_upper.A = np.inf

# do the fit, returns another Params object
popt = fitit.fit(peak, fopt, Pzz, p0, sigma=1, bounds=[p_lower, p_upper])
```

