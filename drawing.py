import schemdraw
import core


def rotation_r(d='down'):
    if d == 'down':
        return 'left'
    if d == 'up':
        return 'right'
    if d == 'left':
        return 'up'
    if d == 'right':
        return 'down'
    
def rotation_l(d='down'):
    if d == 'down':
        return 'right'
    if d == 'up':
        return 'left'
    if d == 'left':
        return 'down'
    if d == 'right':
        return 'up'
    
class CircuitArray(schemdraw.Drawing):
    def __init__(self, unit=3.0, inches_per_unit=0.5, lblofst=0.1,
                 fontsize=14, font='sans-serif', color='black',
                 lw=2, ls='-', fill=None):
        super().__init__(unit=unit, inches_per_unit=inches_per_unit,
                         lblofst=lblofst, fontsize=fontsize, font=font,
                         color=color, lw=lw, ls=ls, fill=fill)

    def series(self, Array, d='down'):
        if isinstance(Array.Elements, core.ExtendedElements):
            self.parallel(Array.Elements, d=d)
        elif not isinstance(Array.Elements, list):
            self.add(Array(d=d))
        else:
            for arr in Array.Elements:
                self.parallel(arr, d=d)
            
    def parallel(self, Array, d='down'):
        if isinstance(Array.Elements, core.ExtendedElements):
            self.series(Array.Elements, d=d)
        elif not isinstance(Array.Elements, list):
            self.add(Array(d=d))
        else:
            length = len(Array)
            self.push()
            for i, arr in enumerate(reversed(Array.Elements[:(length+1)//2])):
                self.pop()
                self.push()
                row = (Array.row-arr.row)/2
                col = Array.col/(length-length%2)*(i+(length+1)%2)
                if not i and length % 2:
                    self.add(core.Dot())
                else:
                    self.add(core.Line(row=col)(d=rotation_r(d=d)))
                self.add(core.Line(row=row)(d=d))
                self.series(arr, d=d)
                self.add(core.Line(row=row)(d=d))
            for arr in Array.Elements[(length+1)//2:]:
                self.pop()
                self.push()
                row = (Array.row-arr.row)/2
                col = Array.col/(length-length%2)*(i+(length+1)%2)
                self.add(core.Line(row=col)(d=rotation_l(d=d)))
                self.add(core.Line(row=row)(d=d))
                self.series(arr, d=d)
                self.add(core.Line(row=row)(d=d))
            self.add(core.Line(row=Array.col/2)(d=rotation_r(d=d)))
            self.push()
            if length % 2:
                self.add(core.Dot())
            self.add(core.Line(row=Array.col/2)(d=rotation_r(d=d)))
            self.pop()
