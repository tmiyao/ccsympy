import sympy
from core import *
from function import *
from drawing import CircuitArray


char = [chr(i) for i in range(97, 123)]
CHAR = [chr(i) for i in range(65, 91)]
num  = [str(i) for i in range(10)]
charnum  = ['%s%s' % (i, j) for j in num for i in char]
CHARnum  = ['%s%s' % (i, j) for j in num for i in CHAR]
charchar = ['%s%s' % (i, j) for j in char for i in char]
CHARCHAR = ['%s%s' % (i, j) for j in CHAR for i in CHAR]
CHARchar = ['%s%s' % (i, j) for j in char for i in CHAR]
LABEL = char+CHAR+num+charnum+CHARnum+charchar+CHARCHAR+CHARchar
ELEMENT = [['C', Capacitance], ['G', Conductance], ['R', Resistance]]
WIRE = Line()
DOT  = Dot()

w   = OMEGA
t   = sympy.Symbol(r'\tau', real=True)
tit = sympy.Symbol(r'\tau_\mathrm{it}', real=True)
tbt = sympy.Symbol(r'\tau_\mathrm{bt}', real=True)

def _EE_Var_global(name, label, Element=None, **kwargs):
    """DO NOT USE in other files!"""
    kwarg = ''
    for k, v in kwargs.items():
        kwarg += ', %s=%s' % (k, v) 
    exec('%s = sympy.Symbol(r\'%s\'%s)' % (name, label, kwarg), globals())
    if Element is not None:
        exec('EE_%s = %s(sym=eval(name))' % (name, Element.__name__), globals())

# define global variables
for i in charnum:
    name = '%s' % i
    label = r'%s' % i
    _EE_Var_global(name, label, real=True)

# define global variables
for i in LABEL:
    for j in ELEMENT:
        name = '%s%s' % (j[0], i)
        label = r'%s_\mathrm{%s}' % (j[0], i)
        Element = j[1]
        _EE_Var_global(name, label, Element, real=True)
