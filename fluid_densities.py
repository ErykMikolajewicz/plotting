from math import e
import scipy.optimize
import numpy as np
''' Note for Python programmers: In this module are used scientific signs of variable, for example T for temperature. 
They are intentionally inconsistent with PEP 8, and not very descriptive.'''


def ro_l_H2O(T):
    Tc = 647.096
    ro_c = 322
    T2 = T
    v = 1 - T2/Tc
    a1 = 1.99274064
    a2 = 1.09965342
    a3 = 0.510839303
    a4 = 1.75493479
    a5 = 45.5170352
    a6 = 6.74694450*10**5
    ro_l = (1 + a1*v**(1/3) + a2*v**(2/3) - a3*v**(5/3) - a4*v**(16/3)
            - a5*v**(43/3) - a6*v**(110/3))*ro_c
    return ro_l


def ro_g_H2O(T):
    Tc = 647.096
    ro_c = 322
    v = 1 - T/Tc
    a1 = 2.03150240
    a2 = 2.68302940
    a3 = 5.38626492
    a4 = 17.2991605
    a5 = 44.7586581
    a6 = 63.79201063
    ro_p = e**(-a1*v**(1/3) - a2*v**(2/3) - a3*v**(4/3) - a4*v**3
               - a5*v**(37/6) - a6*v**(71/6))*ro_c
    return ro_p


def ro_Ar(T, p=101325):
    R = 8.314371
    a, b = 0.1355, 3.2*10**-5
    amount = scipy.optimize.fsolve(lambda n: p - p*n*b + n**2*a - n**3*b*a - n*R*T, 0)
    ro = amount[0] * 0.039948
    return ro


def ro_CO2(T, p=101325):
    R = 8.314371
    a, b = 0.3658, 3.95*10**-5
    amount = scipy.optimize.fsolve(lambda n: p - p*n*b + n**2*a - n**3*b*a - n*R*T, 0)
    ro = amount[0] * 0.044009
    return ro


def ro_N2(T, p=101325):
    R = 8.314371
    a, b = 0.1370, 3.87*10**-5
    amount = scipy.optimize.fsolve(lambda n: p - p*n*b + n**2*a - n**3*b*a - n*R*T, 0)
    ro = amount[0] * 0.028014
    return ro


def ro_O2(T, p=101325):
    R = 8.314371
    a, b = 0.1382, 3.19*10**-5
    amount = scipy.optimize.fsolve(lambda n: p - p*n*b + n**2*a - n**3*b*a - n*R*T, 0)
    ro = amount[0] * 0.031998
    return ro


def Wals_H2O(T, p=101325):
    R = 8.314371
    a, b = 0.55364, 3.05*10**-5
    amount = scipy.optimize.fsolve(lambda n: p - p*n*b + n**2*a - n**3*b*a - n*R*T, 0)
    ro = amount[0] * 0.018015
    return ro


def ro_air(T, p=101325, humidity=0):
    RT = 8.314371*T
    mol_mass = (0.028014, 0.031998, 0.039948, 0.044009, 0.0180155)
    a = np.array([0.1370, 0.1382, 0.1355, 0.3658, 0.55364])
    b = np.array([3.87e-5, 3.19e-5, 3.2e-5, 3.95e-5, 3.05e-5])
    x = np.array([0.78084, 0.20938, 0.009365, 0.000415, 0])
    amount_H2O = ro_g_H2O(T)*humidity/mol_mass[4]
    
    A = (a*a[np.newaxis, :].T)**0.5
    B = (b*b[np.newaxis, :].T)**0.5
    
    flag = 30_000
    while flag:
        X = x*x[np.newaxis, :].T
        a_mix = np.sum(A*X)
        b_mix = np.sum(B*X)
        amount = scipy.optimize.fsolve(lambda n: p*(1 - n*b_mix) + a_mix*(n**2 - n**3*b_mix) - n*RT, 0)
        x[4] = amount_H2O/amount
        to_one = np.sum(x)
        if to_one < 1.001:
            return np.sum(amount*mol_mass*x)
        x[:4] = x[:4]/to_one
        flag -= 1
    raise Exception("Inappropriate  input data")
        
