import sympy
import schemdraw
import schemdraw.elements as elm

OMEGA   = sympy.Symbol(r'\omega', real=True)


class ExtendedElements:
    def __init__(self, Elements=None, row=1, col=1, sym=None, impedance=0):
        self.Elements = Elements
        self.row = row
        self.col = col
        self.sym = sym
        self.impedance = impedance
    
    def convert(self):
        return self.series(self.Elements)
        
    def __len__(self, *args, **kwargs):
        if isinstance(self.Elements, list):
            return len(self.Elements)
        else:
            return 0

    def __repr__(self, *args, **kwargs):
        return self.sym.__repr__(*args, **kwargs)
    
    def __call__(self, d='down'):
        label = r'$'+repr(self.sym)+r'$' if self.sym is not None else None
        return self.Elements(d=d, label=label).length(self.row)
        
    def series(self, Elements):
        if isinstance(Elements, ExtendedElements):
            return Elements
        Arr = [self.parallel(arr) for arr in Elements]
        row = sum(arr.row for arr in Arr)
        col = max(arr.col for arr in Arr)
        sym = [arr.sym for arr in Arr]
        impedance = 0
        for arr in Arr:
            impedance += arr.impedance
        return ExtendedElements(Elements=Arr, row=row, col=col, sym=sym, impedance=impedance)
        
    def parallel(self, Elements):
        if isinstance(Elements, ExtendedElements):
            return Elements
        Arr = [self.series(arr) for arr in Elements]
        row = 2+max(arr.row for arr in Arr)
        col = (len(Arr)+1)//2*2*max(arr.col for arr in Arr)
        sym = [arr.sym for arr in Arr]
        admittance = 0
        for arr in Arr:
            admittance += 1/arr.impedance
        impedance = 1/admittance
        return ExtendedElements(Elements=Arr, row=row, col=col, sym=sym, impedance=impedance)
        
class Dot(ExtendedElements):
    def __init__(self, *args, **kwargs):
        super().__init__(Elements=elm.Dot, row=0, col=0, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.Elements()

class Line(ExtendedElements):
    def __init__(self, *args, **kwargs):
        super().__init__(Elements=elm.Line, *args, **kwargs)

class Capacitance(ExtendedElements):
    def __init__(self, *args, **kwargs):
        super().__init__(Elements=elm.Capacitor, *args, **kwargs)
        self.impedance = 1/(sympy.I*OMEGA*self.sym)
        
class Conductance(ExtendedElements):
    def __init__(self, *args, **kwargs):
        super().__init__(Elements=elm.Resistor, *args, **kwargs)
        self.impedance = 1/self.sym

class Resistance(ExtendedElements):
    def __init__(self, *args, **kwargs):
        super().__init__(Elements=elm.Resistor, *args, **kwargs)
        self.impedance = self.sym
        

