import math

def TeX_code(value):
    '''
    Return TeX code for float value as power of 10

    Input:
    value : numerical value to express as power of 10, e.g. 1e-3

    Returns:
        value to express as power of 10, e.g. 1e-3 as $10^{-3}$

    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com
    
    Created on Mar 8, 2023
    '''
    
    value = abs(value)
    if value > 1.0:
        power = round(math.log10(value))
        return '$10^{' + str(power) + '}$'
    elif value < 1.0:
        power = round(math.log10(value))
        return '$10^{' + str(power) + '}$'
    else:
        return '$10^{0}$'
