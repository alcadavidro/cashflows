"""
This module implements basic functions to compute financial equivalences.

`tvmm` function
===============================================================================


In this example shows how to find different values for a loan of 5000, with a
monthly payment of 130 at the end of the month, a life of 48 periods, and a
interest rate of 0.94 per month (equivalent to 11.32% nominal)

* Periodic payment:

>>> pmt = tvmm(pval=5000, nrate=11.32/12, nper=48, fval=0)
>>> pmt # doctest: +ELLIPSIS
-130.00...

* Future value:

>>> tvmm(pval=5000, nrate=11.32/12, nper=48, pmt=pmt) # doctest: +ELLIPSIS
-0.0...

* Present value:

>>> tvmm(nrate=11.32/12, nper=48, pmt=pmt, fval = 0.0) # doctest: +ELLIPSIS
5000...

* Rate:

>>> tvmm(pval=5000, nper=48, pmt=pmt, fval = 0.0) # doctest: +ELLIPSIS
0.94...

* Number of periods:

>>> tvmm(pval=5000, nrate=11.32/12, pmt=pmt, fval=0.0) # doctest: +ELLIPSIS
48.0...

* Periodic paymnts:

>>> tvmm(pval=5000, nrate=11.32, nper=48, fval=0, pyr=12) # doctest: +ELLIPSIS
-130.00...

* Nominal rate:

>>> tvmm(pval=5000, nper=48, pmt=pmt, fval = 0.0, pyr=12) # doctest: +ELLIPSIS
11.32...




Loan amortization schedule (funtion `amortize`).
==============================================================================



>>> pmt = tvmm(pval=100, nrate=10, nper=5, fval=0) # doctest: +ELLIPSIS
>>> amortize(pval=100, nrate=10, nper=5, fval=0, noprint=False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
t      Beginning     Periodic     Interest    Principal        Final
       Principal      Payment      Payment    Repayment    Principal
          Amount       Amount                                 Amount
--------------------------------------------------------------------
0         100.00         0.00         0.00         0.00       100.00
1         100.00       -26.38        10.00       -16.38        83.62
2          83.62       -26.38         8.36       -18.02        65.60
3          65.60       -26.38         6.56       -19.82        45.78
4          45.78       -26.38         4.58       -21.80        23.98
5          23.98       -26.38         2.40       -23.98         0.00



>>> amortize(pval=-100, nrate=10, nper=5, fval=0, noprint=False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
t      Beginning     Periodic     Interest    Principal        Final
       Principal      Payment      Payment    Repayment    Principal
          Amount       Amount                                 Amount
--------------------------------------------------------------------
0        -100.00         0.00         0.00         0.00      -100.00
1        -100.00        26.38       -10.00        16.38       -83.62
2         -83.62        26.38        -8.36        18.02       -65.60
3         -65.60        26.38        -6.56        19.82       -45.78
4         -45.78        26.38        -4.58        21.80       -23.98
5         -23.98        26.38        -2.40        23.98        -0.00

>>> amortize(pval=100, nrate=10, nper=5, fval=0, due=1, noprint=False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
t      Beginning     Periodic     Interest    Principal        Final
       Principal      Payment      Payment    Repayment    Principal
          Amount       Amount                                 Amount
--------------------------------------------------------------------
0         100.00       -23.98         0.00       -23.98        76.02
1          76.02       -23.98         7.60       -16.38        59.64
2          59.64       -23.98         5.96       -18.02        41.62
3          41.62       -23.98         4.16       -19.82        21.80
4          21.80       -23.98         2.18       -21.80         0.00
5           0.00         0.00         0.00         0.00         0.00

>>> amortize(pval=-100, nrate=10, nper=5, fval=0, due=1, noprint=False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
t      Beginning     Periodic     Interest    Principal        Final
       Principal      Payment      Payment    Repayment    Principal
          Amount       Amount                                 Amount
--------------------------------------------------------------------
0        -100.00        23.98         0.00        23.98       -76.02
1         -76.02        23.98        -7.60        16.38       -59.64
2         -59.64        23.98        -5.96        18.02       -41.62
3         -41.62        23.98        -4.16        19.82       -21.80
4         -21.80        23.98        -2.18        21.80        -0.00
5          -0.00         0.00        -0.00        -0.00        -0.00


>>> principal, interest, payment, balance = amortize(pval=100,
... nrate=10, nper=5, fval=0) # doctest: +ELLIPSIS

>>> principal  # doctest: +ELLIPSIS
[0, -16.37..., -18.01..., -19.81..., -21.80..., -23.98...]

>>> interest  # doctest: +ELLIPSIS
[0, 10.0, 8.36..., 6.56..., 4.57..., 2.39...]

>>> payment  # doctest: +ELLIPSIS
[0, -26.37..., -26.37..., -26.37..., -26.37..., -26.37...]

>>> balance  # doctest: +ELLIPSIS
[100, 83.62..., 65.60..., 45.78..., 23.98..., 1...]

>>> principal, interest, payment, balance = amortize(pval=100,
... nrate=10, nper=5, pmt=pmt) # doctest: +ELLIPSIS

>>> sum(interest)  # doctest: +ELLIPSIS
31.89...

>>> sum(principal)  # doctest: +ELLIPSIS
-99.99...

>>> principal, interest, payment, balance = amortize(fval=0,
... nrate=10, nper=5, pmt=pmt) # doctest: +ELLIPSIS

>>> sum(interest)  # doctest: +ELLIPSIS
31.89...

>>> sum(principal)  # doctest: +ELLIPSIS
-99.99...

>>> principal, interest, payment, balance = amortize(pval=100,
... fval=0, nper=5, pmt=pmt) # doctest: +ELLIPSIS

>>> sum(interest)  # doctest: +ELLIPSIS
31.89...

>>> sum(principal)  # doctest: +ELLIPSIS
-99.99...


>>> amortize(pval=100, fval=0, nrate=10, pmt=pmt, noprint=False) # doctest: +ELLIPSIS
t      Beginning     Periodic     Interest    Principal        Final
       Principal      Payment      Payment    Repayment    Principal
          Amount       Amount                                 Amount
--------------------------------------------------------------------
0         100.00         0.00         0.00         0.00       100.00
1         100.00       -26.38        10.00       -16.38        83.62
2          83.62       -26.38         8.36       -18.02        65.60
3          65.60       -26.38         6.56       -19.82        45.78
4          45.78       -26.38         4.58       -21.80        23.98
5          23.98       -26.38         2.40       -23.98         0.00

>>> principal, interest, payment, balance = amortize(pval=100,
... fval=0, nrate=10, pmt=pmt) # doctest: +ELLIPSIS

>>> sum(interest)  # doctest: +ELLIPSIS
31.89...

>>> sum(principal)  # doctest: +ELLIPSIS
-99.99...



Interest rate transformations (Function `iconv`).
==============================================================================

The function `rate` computes the transformation between nominal, effective and
periodic interest rates. `erate` is the effective rate per year,  `nrate` is the
nominal interest rate per year, and `prate` is the interest rate per period.
`pyr` is the number of compunding periods per year.


**Effective to nominal and periodic rates**.

>>> iconv(erate=10, pyr=12) # doctest: +ELLIPSIS
(9.56..., 0.79...)

>>> iconv(erate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
([9.68..., 9.60..., 9.56...], [3.22..., 1.60..., 0.79...])

>>> iconv(erate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
([9.56..., 11.38..., 13.17...], [0.79..., 0.94..., 1.09...])

>>> iconv(erate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
([9.68..., 11.44..., 13.17...], [3.22..., 1.90..., 1.09...])


**Nominal to effective and periodic rates.**

>>> iconv(nrate=10, pyr=12) # doctest: +ELLIPSIS
(10.47..., 0.83...)

>>> iconv(nrate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
([10.33..., 10.42..., 10.47...], [3.33..., 1.66..., 0.83...])

>>> iconv(nrate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
([10.47..., 12.68..., 14.93...], [0.83..., 1.0, 1.16...])

>>> iconv(nrate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
([10.33..., 12.61..., 14.93...], [3.33..., 2.0, 1.16...])

**Periodic to effective and nominal rates.**

>>> iconv(prate=1, pyr=12) # doctest: +ELLIPSIS
(12, 12.68...)

>>> iconv(prate=1, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
([3, 6, 12], [3.03..., 6.15..., 12.68...])

>>> iconv(prate=[1, 2, 3], pyr=12) # doctest: +ELLIPSIS
([12, 24, 36], [12.68..., 26.82..., 42.57...])

>>> iconv(prate=[1, 2, 3], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
([3, 12, 36], [3.03..., 12.61..., 42.57...])



Description of the functions in this module
==============================================================================


"""

import numpy
from cashflows.gcashcomp import vars2list



def tvmm(pval=None, fval=None, pmt=None, nrate=None, nper=None, due=0, pyr=1, noprint=True):
    """Computes present and future values, interest rate and number
    of periods.

    Args:
        pval (float, list): Present value.
        fval (float, list): Future value.
        pmt (float, list): Periodic payment.
        nrate (float, list): Nominal rate per year.
        nper (int, list): Number of compounding periods.
        due (int): When payments are due.
        pyr (int, list): number of periods per year.
        noprint (bool): prints enhanced output


    Returns:
        Argument set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.


    >>> tvmm(pval=5000, nrate=11.32, nper=48, fval=0, pyr=12, noprint=False) # doctest: +ELLIPSIS
    Present Value: .......  5000.00
    Future Value: ........     0.00
    Payment: .............  -130.01
    Due: .................      END
    No. of Periods: ......    48.00
    Compoundings per Year:    12
    Nominal Rate: .......     11.32
    Effective Rate: .....     11.93
    Periodic Rate: ......      0.94

    >>> tvmm(pval=[5, 500, 5], nrate=11.32, nper=48, fval=0, pyr=12, noprint=False) # doctest: +ELLIPSIS
    #   pval   fval    pmt   nper  nrate  erate  prate due
    ------------------------------------------------------
    0   5.00   0.00  -0.13  48.00  11.32  11.93   0.94 END
    1 500.00   0.00  -0.13  48.00  11.32  11.93   0.94 END
    2   5.00   0.00  -0.13  48.00  11.32  11.93   0.94 END
    """

    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-branches

    numnone = 0
    numnone += 1 if pval is None else 0
    numnone += 1 if fval is None else 0
    numnone += 1 if nper is None else 0
    numnone += 1 if pmt is None else 0
    numnone += 1 if nrate is None else 0

    if numnone > 1:
        raise ValueError('One of the params must be set to None')

    if numnone == 0:
        pmt = None

    if pmt == 0.0:
        pmt = 0.0000001

    nrate = numpy.array(nrate)

    if pval is None:
        result = numpy.pv(rate=nrate/100/pyr, nper=nper, fv=fval, pmt=pmt, when=due)
    elif fval is None:
        result = numpy.fv(rate=nrate/100/pyr, nper=nper, pv=pval, pmt=pmt, when=due)
    elif nper is None:
        result = numpy.nper(rate=nrate/100/pyr, pv=pval, fv=fval, pmt=pmt, when=due)
    elif pmt is None:
        result = numpy.pmt(rate=nrate/100/pyr, nper=nper, pv=pval, fv=fval, when=due)
    else:
        result = numpy.rate(pv=pval, nper=nper, fv=fval, pmt=pmt, when=due) * 100 * pyr

    if noprint is True:
        if isinstance(result, numpy.ndarray):
            return result.tolist()
        return result


    nrate = nrate.tolist()

    if pval is None:
        pval = result
    elif fval is None:
        fval = result
    elif nper is None:
        nper = result
    elif pmt is None:
        pmt = result
    else:
        nrate = result

    params = vars2list([pval, fval, nper, pmt, nrate])
    pval = params[0]
    fval = params[1]
    nper = params[2]
    pmt = params[3]
    nrate = params[4]

    # raise ValueError(nrate.__repr__())

    erate, prate = iconv(nrate=nrate, pyr=pyr)

    if len(pval) == 1:
        if pval is not None:
            print('Present Value: ....... {:8.2f}'.format(pval[0]))
        if fval is not None:
            print('Future Value: ........ {:8.2f}'.format(fval[0]))
        if pmt is not None:
            print('Payment: ............. {:8.2f}'.format(pmt[0]))
        if due is not None:
            print('Due: .................      {:s}'.format('END' if due == 0 else 'BEG'))
        print('No. of Periods: ...... {:8.2f}'.format(nper[0]))
        print('Compoundings per Year: {:>5d}'.format(pyr))
        print('Nominal Rate: .......  {:8.2f}'.format(nrate[0]))
        print('Effective Rate: .....  {:8.2f}'.format(erate))
        print('Periodic Rate: ......  {:8.2f}'.format(prate))

    else:
        if due == 0:
            sdue = 'END'
            txtpmt = []
            for item, _ in enumerate(pval):
                txtpmt.append(pmt[item][-1])
        else:
            sdue = 'BEG'
            txtpmt = []
            for item, _ in enumerate(pval):
                txtpmt.append(pmt[item][0])


        maxlen = 5
        for value1, value2, value3, value4 in zip(pval, fval, txtpmt, nper):
            maxlen = max(maxlen, len('{:1.2f}'.format(value1)))
            maxlen = max(maxlen, len('{:1.2f}'.format(value2)))
            maxlen = max(maxlen, len('{:1.2f}'.format(value3)))
            maxlen = max(maxlen, len('{:1.2f}'.format(value4)))

        len_aux = len('{:d}'.format(len(pval)))

        fmt_num = ' {:' + '{:d}'.format(maxlen) + '.2f}'
        fmt_num = '{:<' + '{:d}'.format(len_aux) +  'd}' + fmt_num * 7 + ' {:3s}'
        # fmt_shr = '{:' + '{:d}'.format(len_aux) + 's}'
        fmt_hdr = ' {:>' + '{:d}'.format(maxlen) + 's}'
        fmt_hdr = '{:' + '{:d}'.format(len_aux) + 's}' + fmt_hdr * 7 + ' due'


        txt = fmt_hdr.format('#', 'pval', 'fval', 'pmt', 'nper', 'nrate', 'erate', 'prate')
        print(txt)
        print('-' * len_aux + '-' * maxlen * 7 + '-' * 7 + '----')
        for item, _ in enumerate(pval):
            print(fmt_num.format(item,
                                 pval[item],
                                 fval[item],
                                 txtpmt[item],
                                 nper[item],
                                 nrate[item],
                                 erate[item],
                                 prate[item],
                                 sdue))


def pvfv(pval=None, fval=None, nrate=None, nper=None, pyr=1, noprint=True):
    """Computes interest rate parameters.

    Args:
        pval (float, list): Present value.
        fval (float, list): Future value.
        nrate (float, list): Nominal rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    return tvmm(pval=pval, fval=fval, pmt=0, nrate=nrate, nper=nper, due=0, pyr=pyr, noprint=noprint)


def pmtfv(pmt=None, fval=None, nrate=None, nper=None, pyr=1, noprint=True):
    """Computes interest rate parameters for periodic payments.

    Args:
        pmt (float, list): Periodic payment.
        fval (float, list): Future value.
        nrate (float, list): Nominal rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    return tvmm(pval=0, fval=fval, pmt=pmt, nrate=nrate, nper=nper, due=0, pyr=pyr, noprint=noprint)


def pvpmt(pmt=None, pval=None, nrate=None, nper=None, pyr=1, noprint=True):
    """Computes interest rate parameters for periodic payments.

    Args:
        pmt (float, list): Periodic payment.
        pval (float, list): Present value.
        nrate (float, list): Nominal rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    return tvmm(pval=pval, fval=0, pmt=pmt, nrate=nrate, nper=nper, due=0, pyr=pyr, noprint=noprint)


def amortize(pval=None, fval=None, pmt=None, nrate=None, nper=None, due=0, pyr=1, noprint=True):
    """Amortization schedule of a loan.

    Args:
        pval (float): present value.
        fval (float): Future value.
        pmt (float): periodic payment per period.
        nrate (float): nominal rate per year.
        nper (int): total number of compounding periods.
        due (int): When payments are due.
        pyr (int, list): number of periods per year.

    Returns:
        A tuple: (principal, interest, payment, balance)


    """

    #pylint: disable=too-many-arguments


    numnone = 0
    numnone += 1 if pval is None else 0
    numnone += 1 if fval is None else 0
    numnone += 1 if nper is None else 0
    numnone += 1 if pmt is None else 0
    numnone += 1 if nrate is None else 0


    if numnone > 1:
        raise ValueError('One of the params must be set to None')

    if numnone == 0:
        pmt = None

    if pmt == 0.0:
        pmt = 0.0000001

    if pval is None:
        pval = tvmm(fval=fval, pmt=pmt, nrate=nrate, nper=nper, due=due, pyr=pyr)
    elif fval is None:
        fval = tvmm(pval=pval, pmt=pmt, nrate=nrate, nper=nper, due=due, pyr=pyr)
    elif nper is None:
        nper = tvmm(pval=pval, fval=fval, pmt=pmt, nrate=nrate, due=due, pyr=pyr)
    elif pmt is None:
        pmt = tvmm(pval=pval, fval=fval, nrate=nrate, nper=nper, due=due, pyr=pyr)
    else:
        nrate = tvmm(pval=pval, fval=fval, pmt=pmt, nper=nper, due=due, pyr=pyr)

    erate = nrate / pyr / 100

    if int(nper) != nper:
        nper = int(nper + 0.9)

    # variable definition
    begbal = [0] * (nper + 1)
    ipmt = [0] * (nper + 1)
    ppmt = [0] * (nper + 1)
    rembal = [0] * (nper + 1)

    # calcula el pmt periodico
    pmt = [pmt] * (nper + 1)

    if due == 0:  # vencido
        pmt[0] = 0

    if due == 1:  # anticipado
        pmt[nper] = 0

    begbal[0] = pval


    for period in range(nper + 1):

        if period == 0:
            rembal[0] = begbal[0] + pmt[0]
            ppmt[0] = + pmt[0]
        else:
            begbal[period] = rembal[period-1]
            ipmt[period] = begbal[period] * erate
            ppmt[period] = pmt[period] + ipmt[period]
            rembal[period] = begbal[period] + ppmt[period]

    if noprint is True:
        return (ppmt, ipmt, pmt, rembal)

    txt = ['t      Beginning     Periodic     Interest    Principal        Final',
           '       Principal      Payment      Payment    Repayment    Principal',
           '          Amount       Amount                                 Amount',
           '--------------------------------------------------------------------']

    for time in range(nper + 1):

        fmt = '{:<3d} {:12.2f} {:12.2f} {:12.2f} {:12.2f} {:12.2f}'


        txt.append(fmt.format(time,
                              begbal[time],
                              pmt[time],
                              ipmt[time],
                              ppmt[time],
                              rembal[time]))
    print('\n'.join(txt))
    return None

def iconv(nrate=None, erate=None, prate=None, pyr=1):
    """Transformations between nominal and effective annual interest rate.

    Args:
        nrate (float, list): nominal interest rate per year.
        erate (float, list): effective interest rate per year.
        prate (float, list): periodic rate
        pyr (int, list): number of periods per year

    Returns:
        `(nrate, prate)`: when `erate` is specified
        `(erate, prate)`: when `nrate` is specified
        `(nrate, erate)`: when `prate` is specified
    """

    numnone = 0
    if nrate is None:
        numnone += 1
    if erate is None:
        numnone += 1
    if prate is None:
        numnone += 1
    if numnone != 2:
        raise ValueError('Two of the rates must be set to `None`')

    if isinstance(nrate, list) and isinstance(pyr, list) and len(nrate) != len(pyr):
        raise ValueError('List must have the same length')
    if isinstance(erate, list) and isinstance(pyr, list) and len(erate) != len(pyr):
        raise ValueError('List must have the same length')
    if isinstance(prate, list) and isinstance(pyr, list) and len(prate) != len(pyr):
        raise ValueError('List must have the same length')

    maxlen = 1
    if isinstance(nrate, list):
        maxlen = max(maxlen, len(nrate))
    if isinstance(erate, list):
        maxlen = max(maxlen, len(erate))
    if isinstance(prate, list):
        maxlen = max(maxlen, len(prate))
    if isinstance(pyr, list):
        maxlen = max(maxlen, len(pyr))

    if isinstance(pyr, (int, float)):
        pyr = [pyr] * maxlen
    pyr = numpy.array(pyr)

    if nrate is not None:
        if isinstance(nrate, (int, float)):
            nrate = [nrate] * maxlen
        nrate = numpy.array(nrate)
        prate = nrate / pyr
        erate = 100 * (numpy.power(1 + prate/100, pyr) - 1)
        prate = prate.tolist()
        erate = erate.tolist()
        if maxlen == 1:
            prate = prate[0]
            erate = erate[0]
        return (erate, prate)

    if erate is not None:
        if isinstance(erate, (int, float)):
            erate = [erate] * maxlen
        erate = numpy.array(erate)
        prate = 100 * (numpy.power(1 + erate / 100, 1 / pyr) - 1)
        nrate = pyr * prate
        prate = prate.tolist()
        nrate = nrate.tolist()
        if maxlen == 1:
            prate = prate[0]
            nrate = nrate[0]
        return (nrate, prate)

    if isinstance(prate, (int, float)):
        prate = [prate] * maxlen
    prate = numpy.array(prate)
    erate = 100 * (numpy.power(1 + prate / 100, pyr) - 1)
    nrate = pyr * prate
    erate = erate.tolist()
    nrate = nrate.tolist()
    if maxlen == 1:
        erate = erate[0]
        nrate = nrate[0]
    return (nrate, erate)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
