"""

Cashflow taxing
===============================================================================

The function `after_tax_cashflow` returns a new cashflow object for which the
values are taxed. The specified tax rate is only appled to positive values
in the cashflow. Negative values are reemplazed by a zero value. `Cashflow`
and `Rate` must have the same length.


>>> cflo = cashflow(const_value=[100] * 5, spec=(0, -100))
>>> tax_rate = nominal_rate(const_value=[10] * 5)
>>> after_tax_cashflow(cflo=cflo, tax_rate=tax_rate) # doctest: +NORMALIZE_WHITESPACE
Time Series:
Start = (0,)
End = (4,)
pyr = 1
Data = (0,)           0.00
       (1,)-(4,) [4] 10.00

Constant and current dollars transformations
===============================================================================

**Constant to current.**

>>> const2curr(cflo=cashflow(const_value=[100] * 5),
... inflation=nominal_rate(const_value=[10, 10, 20, 20, 20])) # doctest: +NORMALIZE_WHITESPACE
Time Series:
Start = (0,)
End = (4,)
pyr = 1
Data = (0,)   100.00
       (1,)   110.00
       (2,)   132.00
       (3,)   158.40
       (4,)   190.08


>>> const2curr(cflo=cashflow(const_value=[100] * 5),
... inflation=nominal_rate(const_value=[10, 10, 20, 20, 20]), base_date=4) # doctest: +NORMALIZE_WHITESPACE
Time Series:
Start = (0,)
End = (4,)
pyr = 1
Data = (0,)    52.61
       (1,)    57.87
       (2,)    69.44
       (3,)    83.33
       (4,)   100.00


**Current dollars to constant dollars.**

>>> curr2const(cflo=cashflow(const_value=[100] * 5),
... inflation=nominal_rate(const_value=[10, 10, 20, 20, 20])) # doctest: +NORMALIZE_WHITESPACE
Time Series:
Start = (0,)
End = (4,)
pyr = 1
Data = (0,)   100.00
       (1,)    90.91
       (2,)    75.76
       (3,)    63.13
       (4,)    52.61

>>> curr2const(cflo=cashflow(const_value=[100] * 5),
... inflation=nominal_rate(const_value=[10, 10, 20, 20, 20]), base_date=4) # doctest: +NORMALIZE_WHITESPACE
Time Series:
Start = (0,)
End = (4,)
pyr = 1
Data = (0,)   190.08
       (1,)   172.80
       (2,)   144.00
       (3,)   120.00
       (4,)   100.00



Currency conversion
===============================================================================

>>> currency_conversion(cflo=cashflow(const_value=[100] * 5), exchange_rate = 2) # doctest: +NORMALIZE_WHITESPACE
Time Series:
Start = (0,)
End = (4,)
pyr = 1
Data = (0,)-(4,) [5] 200.00

>>> currency_conversion(cflo=cashflow(const_value=[100] * 5), exchange_rate = 2,
... devaluation=nominal_rate(const_value=[5]*5), base_date=(2,)) # doctest: +NORMALIZE_WHITESPACE
Time Series:
Start = (0,)
End = (4,)
pyr = 1
Data = (0,)   181.41
       (1,)   190.48
       (2,)   200.00
       (3,)   210.00
       (4,)   220.50



Description of the functions in this module
===============================================================================


"""

from cashflows.gtimeseries import TimeSeries, cashflow, nominal_rate, verify_eq_time_range, _timeid2index

def vars2list(params):
    """ Converts the variables on lists of the same length
    """
    length = 1
    for param in params:
        if isinstance(param, list):
            length = max(length, len(param))
    if length > 1:
        for param in params:
            if isinstance(param, list) and len(param) != length:
                raise Exception('Lists in parameters must the same length')
    result = []
    for param in params:
        if isinstance(param, list):
            result.append(param)
        else:
            result.append([param] * length)
    return result


def after_tax_cashflow(cflo, tax_rate):
    """Computes the after cashflow for a tax rate. Taxes are not computed
    for negative values in the cashflow.

    Args:
        cflo (TimeSeries): generic cashflow.
        tax_rate (TimeSeries): income tax rate.

    Returns:
        TimeSeries objects with taxed values


    >>> cflo = cashflow(const_value=[100] * 5, spec=(0, -100))
    >>> tax_rate = nominal_rate(const_value=[10] * 5)
    >>> after_tax_cashflow(cflo=cflo, tax_rate=tax_rate) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)           0.00
           (1,)-(4,) [4] 10.00

    """
    params = vars2list([cflo, tax_rate])
    cflo = params[0]
    tax_rate = params[1]
    retval = []
    for xcflo, xtax_rate in zip(cflo, tax_rate):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("cashflow must be a TimeSeries")
        verify_eq_time_range(xcflo, xtax_rate)
        result = xcflo.copy()
        for time, _ in enumerate(xcflo):
            if result[time] > 0:
                result[time] *= xtax_rate[time] / 100
            else:
                result[time] = 0
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval





def to_discount_factor(nrate, base_date=0):
    """Returns a list of discount factors calculated as 1 / (1 + r)^(t - t0).

    Args:
        nrate (TimeSeries): nominal interest rate.
        base_date (int, tuple): basis time.

    Returns:
        Discount factor (list)


    >>> to_discount_factor(nominal_rate(const_value=4,nper=12, pyr=4), base_date=2) # doctest: +ELLIPSIS
    [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]


    >>> to_discount_factor(nominal_rate(const_value=4,nper=12, pyr=4), base_date=(0, 2)) # doctest: +ELLIPSIS
    [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]

    """

    prate = [x/nrate.pyr/100 for x in nrate.data]  # periodic rate
    factor = prate.copy()
    for index, _ in enumerate(factor):
        if index == 0:
            factor[0] = 1 / (1 + factor[0])
        else:
            factor[index] = factor[index-1] / (1 + factor[index])
    if isinstance(base_date, tuple):
        base_date = _timeid2index(base_date, basis=nrate.start, pyr=nrate.pyr)
    div = factor[base_date]
    for index, _ in enumerate(factor):
        factor[index] = factor[index] / div
    return factor


def to_compound_factor(nrate, base_date=0):
    """Returns a list of compounding factors calculated as (1 + r)^(t - t0).

    Args:
        nrate (TimeSeries): nominal interest rate.
        base_date (int, tuple): basis time.

    Returns:
        Compound factor (list)

    >>> to_compound_factor(nominal_rate(const_value=4,nper=10, pyr=4), base_date=2) # doctest: +ELLIPSIS
    [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]

    >>> to_compound_factor(nominal_rate(const_value=4,nper=12, pyr=4), base_date=(0, 2)) # doctest: +ELLIPSIS
    [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]

    """
    factor = to_discount_factor(nrate, base_date)
    for time, _ in enumerate(factor):
        factor[time] = 1 / factor[time]
    return factor



def equivalent_nrate(nrate):
    """Returns the equivalent interest rate over a time period.

    # >>> equivalent_nrate(TimeSeries([10]*5)) # doctest: +ELLIPSIS
    # 10.0...
    """
    value = nrate.tolist()
    factor = 1
    for element in value[1:]:
        factor *= (1 + element / 100 / nrate.pyr)
    return 100 * nrate.pyr * (factor**(1/(len(value) - 1)) - 1)




def const2curr(cflo, inflation, base_date=0):
    """Converts a cashflow of constant dollars to current dollars
    of the time `base_date`.

    Args:
        cflo (TimeSeries): A cashflow.
        inflation (TimeSeries): Inflation rate.
        base_date (int, tuple): base time.

    Returns:
        A cashflow in current money (TimeSeries)

    >>> const2curr(cflo=cashflow(const_value=[100] * 5),
    ... inflation=nominal_rate(const_value=[10, 10, 20, 20, 20])) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)   100.00
           (1,)   110.00
           (2,)   132.00
           (3,)   158.40
           (4,)   190.08


    """
    params = vars2list([cflo, inflation, base_date])
    cflo = params[0]
    inflation = params[1]
    base_date = params[2]
    retval = []
    for xcflo, xinflation, xbase_date in zip(cflo, inflation, base_date):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("cflo must be a TimeSeries object")
        if not isinstance(xinflation, TimeSeries):
            raise TypeError("inflation must be a TimeSeries object")
        verify_eq_time_range(xcflo, xinflation)
        factor = to_compound_factor(xinflation, xbase_date)
        result = xcflo.copy()
        for time, _ in enumerate(result):
            result[time] *= factor[time]
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval



def curr2const(cflo, inflation, base_date=0):
    """Converts a cashflow of current dollars to constant dollars of
    the time `t0`.

    Args:
        cflo (list, Cashflow): A cashflow.
        inflation_rate (float, Rate): Inflation rate.
        t0 (int): base time.

    Returns:
        A cashflow in constant dollars

    >>> curr2const(cflo=cashflow(const_value=[100] * 5),
    ... inflation=nominal_rate(const_value=[10, 10, 20, 20, 20])) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)   100.00
           (1,)    90.91
           (2,)    75.76
           (3,)    63.13
           (4,)    52.61

    """
    params = vars2list([cflo, inflation, base_date])
    cflo = params[0]
    inflation = params[1]
    base_date = params[2]
    retval = []
    for xcflo, xinflation, xbase_date in zip(cflo, inflation, base_date):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("cflo must be a TimeSeries object")
        if not isinstance(xinflation, TimeSeries):
            raise TypeError("inflation must be a TimeSeries object")
        verify_eq_time_range(xcflo, xinflation)
        factor = to_discount_factor(xinflation, xbase_date)
        result = xcflo.copy()
        for time, _ in enumerate(result):
            result[time] *= factor[time]
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval


def currency_conversion(cflo, exchange_rate=1, devaluation=None, base_date=0):
    """Converts a cashflow of dollars to another currency.

    Args:
        cflo (TimeSeries): A cashflow.
        exchange_rate (float): Exchange rate at time `base_date`.
        devaluaton (TimeSeries): Devaluation rate.
        base_date (int): Time.

    Returns:
        A cashflow in other currency.




    """
    params = vars2list([cflo, exchange_rate, devaluation, base_date])
    cflo = params[0]
    exchange_rate = params[1]
    devaluation = params[2]
    base_date = params[3]
    retval = []
    for xcflo, xexchange_rate, xdevaluation, xbase_date in zip(cflo, exchange_rate, devaluation, base_date):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("`cashflow` must be a TimeSeries")
        if xdevaluation is None:
            result = xcflo.copy()
            for time, _ in enumerate(result):
                result[time] *= xexchange_rate
        else:
            if not isinstance(xdevaluation, TimeSeries):
                raise TypeError("`devaluation` must be a TimeSeries")
            verify_eq_time_range(xcflo, xdevaluation)
            factor = to_compound_factor(xdevaluation, xbase_date)
            result = xcflo.copy()
            for time, _ in enumerate(result):
                result[time] *= xexchange_rate * factor[time]
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval

if __name__ == "__main__":
    import doctest
    doctest.testmod()
