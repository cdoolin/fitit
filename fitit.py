VERSION = 4
from scipy import optimize


# utility class to keep track of fitting parameters.  Can both accept a ndarray 
# and convert to named parameters and generate a ndarray for use with leastsq.
class Params(object):
    def __init__(self, params="", like=None, vals=[], fitvals=[], fiterrs=[], fitinfo=None):
        self.errors = {}
        self.fitinfo = fitinfo
        if like is not None:
            # copy params from reference Params object
            self.params = like.params[:]
            self.tofit  = like.tofit[:]
            for p in self.params:
                self.__setattr__(p, like.__getattribute__(p))
        else:
            # parse params string for parameters
            ps = params.split()
            self.params = [p.replace('*', '') for p in ps]
            self.tofit = [p.find('*') is -1 for p in ps]
            for p in self.params:
                self.__setattr__(p, 1)

        if len(vals) > 0:
            self.set_vals(vals)
        if len(fitvals) > 0:
            self.set_fitvals(fitvals)
        if len(fiterrs) > 0:
            self.set_fiterrs(fiterrs)
        else:
            self.has_errors = False

    
    def keys(self):
        return " ".join(self.params)

    def fitparams(self):
        return [p for p, t in zip(self.params, self.tofit) if t]
            
    def fitvals(self):
        return [self.__getattribute__(p) for p in self.fitparams()]

    def set_fitvals(self, vals):
        for p, v in zip(self.fitparams(), vals):
            self.__setattr__(p, v)

    def set_fiterrs(self, vals):
        for p, v in zip(self.fitparams(), vals):
            self.errors[p] = v
            # self.__setattr__(p + 'e', v)

    def set_vals(self, args):
        for p, v in zip(self.params, args):
            self.__setattr__(p, v)
        self.has_errors = True

    def __repr__(self):
        padding = max([len(p) for p in self.params]) + 1
        instr = "%" + str(padding) + "s: %f"
        return "\n".join(
            [instr % (p, self.__getattribute__(p)) for p in self.params])


    def with_const(self, **kwargs):
        # create a copy of the params with each keyword to with set as constants.
        p = Params(like=self)
        for k, v in kwargs.items():
            p.tofit[p.params.index(k)] = False
            p.__setattr__(k, v)
        return p

    def with_(self, **kwargs):
        # create a copy with keywards changed. Don't modify whats constant.
        p = Params(like=self)
        for k, v in kwargs.items():
            p.__setattr__(k, v)
        return p


def fit(func, x, y, p0, sigma=1., fitinfo=False, fillbaderrs=None):
    def residual(params):
        p = Params(like=p0, fitvals=params)
        return abs(func(x, p) - y) / sigma
        
    # taken from scipy's curve_fit
    r = optimize.leastsq(residual, p0.fitvals(), full_output=True)
    popt, pcov, info, errmsg, ier = r

    if ier not in [1, 2, 3, 4]:
        print("Warning, optimal parameters not found: " + errmsg)
        #raise RuntimeError(msg)

    if (len(y) > len(p0.fitparams())) and pcov is not None:
        s_sq = (residual(popt)**2).sum()/(len(y)-len(p0.fitparams()))
        pcov = pcov * s_sq
        # diagonal should be variance
        errs = pcov.diagonal()**0.5
    else:
        print("could not determine fit errors:\n%s" % errmsg)
        if fillbaderrs is None:
            errs = []
        else:
            errs = [fillbaderrs] * len(p0.fitparams())

    if fitinfo:
        return Params(like=p0, fitvals=popt, fiterrs=errs, fitinfo=r), r
    else:
        return Params(like=p0, fitvals=popt, fiterrs=errs, fitinfo=r)

