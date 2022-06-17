import sympy
from core import ExtendedElements


def EE_Variable(Element, label, **kwargs):
    sym = sympy.Symbol(label, **kwargs)
    elm = Element(sym=sym)
    return sym, elm

def EE_convert(array):
    if isinstance(array, ExtendedElements):
        return array.impedance
    elif isinstance(array, list):
        return [EE_convert(arr) for arr in array]
    elif isinstance(array, tuple):
        return tuple(EE_convert(arr) for arr in array)
    elif isinstance(array, dict):
        return {EE_convert(k) : EE_convert(v) for k, v in array.items()}
    else:
        return array

def EE_integrate(func):
    def inner(*args, **kwargs):
        args = EE_convert(args)
        kwargs = EE_convert(kwargs)
        return func(*args, **kwargs)
    return inner

def reprEq(param, result, verbose):
    eqs = []
    if type(result) == dict:
        for k, v in result.items():
            eq = sympy.Eq(k, v)
            eqs.append(eq)
    elif type(result[0]) == dict:
        for r in result:
            for k, v in r.items():
                eq = sympy.Eq(k, v)
                eqs.append(eq)
    else:
        for res in result:
            eqs_ = []
            for i, prm in enumerate(param):
                eq = sympy.Eq(prm, res[i])
                eqs_.append(eq)
            eqs.append(eqs_)

    if verbose:
        print('\n')
        for eq in eqs:
            print(sympy.latex(eq))
        print('\n')
    return eqs

@EE_integrate
def EE_solve_complex(param, el, eq=[], verbose=False):
    eq1 = sympy.Eq(sympy.re(el[0]), sympy.re(el[1]))
    eq2 = sympy.Eq(sympy.im(el[0]), sympy.im(el[1]))
    ans = sympy.solve([eq1, eq2]+eq, param)
    eqs = reprEq(param, ans, verbose)
    return eqs

@EE_integrate
def decode_Eq(param, eqs):
    if isinstance(eqs, list):
        arr = [decode_Eq(param, eq) for eq in eqs]
        arr = [arg for arg in arr if arg]
        if len(arr) == 1:
            return arr[0]
        else:
            return arr
    else:
        for k, v in sympy.solve(eqs)[0].items():
            if k == param:
                return v
        return None

@EE_integrate
def EE_subs(param, func):
    return func.subs(param)

@EE_integrate
def EE_lambdify(args, func):
    return sympy.lambdify(args, func, 'numpy')

