# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, 2017 Caleb Bell <Caleb.Andrew.Bell@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

from __future__ import division
from math import log, exp, pi
from scipy.constants import g
from scipy.interpolate import UnivariateSpline
from scipy.constants import foot, psi

__all__ = ['v_Sounders_Brown', 'K_separator_Watkins',
           'K_separator_demister_York', 'K_Sounders_Brown_theoretical']


# 92 points taken from a 2172x3212 page scan, after dewarping the scan,
# digitization with Engauge Digitizer, and extensive checking; every 5th point 
# it produced was selected plus the last point. The initial value is adjusted 
# to be the lower limit of the graph.

v_factors_Watkins = [0.006, 0.00649546, 0.00700535, 0.00755527, 0.00817788,
    0.00881991, 0.00954676, 0.0103522, 0.0112256, 0.0121947, 0.0132476,
    0.0143655, 0.0156059, 0.0169841, 0.018484, 0.0201165, 0.0219329,
    0.0239133, 0.0260727, 0.0284272, 0.0309944, 0.0339158, 0.037046,
    0.0403924, 0.0441998, 0.0483665, 0.0529259, 0.0579153, 0.0632613,
    0.0692251, 0.0756157, 0.0825962, 0.0902214, 0.0983732, 0.107262,
    0.116954, 0.127753, 0.139047, 0.151614, 0.165317, 0.179934, 0.195845,
    0.21278, 0.231181, 0.251627, 0.272897, 0.295966, 0.32041, 0.347497,
    0.3762, 0.407274, 0.440914, 0.476478, 0.513983, 0.554442, 0.59701,
    0.642851, 0.690966, 0.744018, 0.798268, 0.856477, 0.920588, 0.987716,
    1.05784, 1.13294, 1.21337, 1.29718, 1.38678, 1.4799, 1.58212, 1.68837,
    1.79851, 1.91583, 2.04083, 2.16616, 2.29918, 2.44037, 2.59025, 2.73944,
    2.89725, 3.06414, 3.24064, 3.42731, 3.61822, 3.81976, 4.02527, 4.24949,
    4.47008, 4.71907, 4.96404, 5.22172, 5.43354]

Kv_Watkins = [0.23722, 0.248265, 0.260298, 0.272915, 0.284578, 0.297283,
    0.309422, 0.322054, 0.33398, 0.345714, 0.355905, 0.366397, 0.377197,
    0.386898, 0.396125, 0.404831, 0.411466, 0.41821, 0.424289, 0.428886,
    0.433533, 0.435832, 0.436547, 0.436468, 0.437982, 0.437898, 0.437815,
    0.436932, 0.435258, 0.434381, 0.431138, 0.427919, 0.42395, 0.420018,
    0.415364, 0.410012, 0.403988, 0.39733, 0.390067, 0.38154, 0.373883,
    0.364378, 0.354467, 0.344197, 0.333613, 0.322767, 0.311704, 0.299923,
    0.289114, 0.277173, 0.265725, 0.254749, 0.243338, 0.232438, 0.221621,
    0.211309, 0.200742, 0.190704, 0.181498, 0.172108, 0.162906, 0.154196,
    0.145952, 0.137897, 0.130049, 0.122647, 0.115667, 0.108885, 0.102502,
    0.0963159, 0.0903385, 0.0847323, 0.0796194, 0.0744062, 0.0695348,
    0.0651011, 0.060839, 0.0567521, 0.0529401, 0.0492041, 0.0458154,
    0.0426601, 0.039722, 0.036919, 0.0343137, 0.0318924, 0.0296419,
    0.0275001, 0.0255595, 0.0237127, 0.0219993, 0.0207107]
Watkins_interp = UnivariateSpline(v_factors_Watkins, Kv_Watkins, s=.00001)


def K_separator_Watkins(x, rhol, rhog, horizontal=False, method='spline'):
    r'''Calculates the Sounders-Brown `K` factor as used in determining maximum 
    allowable gas velocity in a two-phase separator in either a horizontal or
    vertical orientation. This function approximates a graph published in [1]_ 
    to determine `K` as used in the following equation:
    
    .. math::
        v_{max} =  K_{SB}\sqrt{\frac{\rho_l-\rho_g}{\rho_g}}
    
    The graph has `K_{SB}` on its y-axis, and the following as its x-axis:
    
    .. math::
        \frac{m_l}{m_g}\sqrt{\rho_g/\rho_l}
        = \frac{(1-x)}{x}\sqrt{\rho_g/\rho_l}
    
    Cubic spline interpolation is the default method of retrieving a value
    from the graph, which was digitized with Engauge-Digitizer.
    
    Also supported are two published curve fits to the graph. The first is that
    of Blackwell (1984) [2]_, as follows:
    
    .. math::
        K_{SB} = \exp(-1.942936 -0.814894X -0.179390 X^2 -0.0123790 X^3
        + 0.000386235 X^4 + 0.000259550 X^5)

        X = \log\left[\frac{(1-x)}{x}\sqrt{\rho_g/\rho_l}\right]
    
    The second is that of Branan (1999), as follows:
    
    .. math::
        K_{SB} = \exp(-1.877478097 -0.81145804597X -0.1870744085 X^2 
        -0.0145228667 X^3 -0.00101148518 X^4)
    
        X = \log\left[\frac{(1-x)}{x}\sqrt{\rho_g/\rho_l}\right]

    Parameters
    ----------
    x : float
        Quality of fluid entering separator, [-]
    rhol : float
        Density of liquid phase [kg/m^3]
    rhog : float
        Density of gas phase [kg/m^3]
    horizontal : bool, optional
        Whether to use the vertical or horizontal value; horizontal is 1.25 
        higher
    method : str
        One of 'spline, 'blackwell', or 'branan'

    Returns
    -------
    K : float
        Sounders Brown horizontal or vertical `K` factor for two-phase 
        separator design only, [m/s]

    Notes
    -----
    Both the 'branan' and 'blackwell' models are used frequently. However,
    the spline is much more accurate.
    
    No limits checking is enforced. However, the x-axis spans only 0.006 to
    5.4, and the function should not be used outside those limits.

    Examples
    --------
    >>> K_separator_Watkins(0.88, 985.4, 1.3, horizontal=True)
    0.07944704064029771

    References
    ----------
    .. [1] Watkins (1967). Sizing Separators and Accumulators, Hydrocarbon 
       Processing, November 1967.
    .. [2] Blackwell, W. Wayne. Chemical Process Design on a Programmable 
       Calculator. New York: Mcgraw-Hill, 1984.
    .. [3] Branan, Carl R. Pocket Guide to Chemical Engineering. 1st edition. 
       Houston, Tex: Gulf Professional Publishing, 1999.
    '''
    factor = (1. - x)/x*(rhog/rhol)**0.5
    if method == 'spline':
        K = float(Watkins_interp(factor))
    elif method == 'blackwell':
        X = log(factor)    
        A = -1.877478097
        B = -0.81145804597
        C = -0.1870744085
        D = -0.0145228667
        E = -0.00101148518
        K = exp(A + X*(B + X*(C + X*(D + E*X))))
    elif method == 'branan':
        X = log(factor)
        A = -1.942936
        B = -0.814894
        C = -0.179390
        D = -0.0123790
        E = 0.000386235
        F = 0.000259550
        K = exp(A + X*(B + X*(C + X*(D + X*(E + F*X)))))
    else:
        raise Exception("Only methods 'spline', 'branan', and 'blackwell' are supported.")
    K *= foot # Converts units of ft/s to m/s; the graph and all fits are in ft/s 
    if horizontal:
        K *= 1.25 # Watkins recommends a factor of 1.25 for horizontal separators over vertical separators
    return K


def K_separator_demister_York(P, horizontal=False):
    r'''Calculates the Sounders Brown `K` factor as used in determining maximum 
    permissible gas velocity in a two-phase separator in either a horizontal or 
    vertical orientation, *with a demister*.
    This function is a curve fit to [1]_ published in [2]_ and is widely used. 
    
    For 1 < P < 15 psia:   
    
    .. math::
        K = 0.1821 + 0.0029P + 0.0460\ln P

    For 15 <= P <= 40 psia:   
    
    .. math::
        K = 0.35
        
    For P < 5500 psia:
    
    .. math::
        K = 0.430 - 0.023\ln P
        
    In the above equations, P is in units of psia.

    Parameters
    ----------
    P : float
        Pressure of separator, [Pa]
    horizontal : bool, optional
        Whether to use the vertical or horizontal value; horizontal is 1.25 
        times higher, [-]

    Returns
    -------
    K : float
        Sounders Brown Horizontal or vertical `K` factor for two-phase
        separator design with a demister, [m/s]

    Notes
    -----
    If the input pressure is under 1 psia, 1 psia is used. If the
    input pressure is over 5500 psia, 5500 psia is used.

    Examples
    --------
    >>> K_separator_demister_York(975*psi)
    0.08281536035331669

    References
    ----------
    .. [2] Otto H. York Company, "Mist Elimination in Gas Treatment Plants and 
       Refineries," Engineering, Parsippany, NJ.
    .. [1] Svrcek, W. Y., and W. D. Monnery. "Design Two-Phase Separators 
       within the Right Limits" Chemical Engineering Progress, (October 1, 
       1993): 53-60.
    '''
    P = P/psi # Correlation in terms of psia
    if P < 15:
        if P < 1: 
            P = 1 # Prevent negative K values, but as a consequence be  
            # optimistic for K values; limit is 0.185 ft/s but real values
            # should probably be lower
        K = 0.1821 + 0.0029*P + 0.0460*log(P)
    elif P < 40:
        K = 0.35
    else:
        if P > 5500:
            P = 5500 # Do not allow for lower K values above 5500 psia, as
            # the limit is stated to be 5500
        K = 0.430 - 0.023*log(P)
    K *= foot # Converts units of ft/s to m/s; the graph and all fits are in ft/s 
    if horizontal:
        # Watkins recommends a factor of 1.25 for horizontal separators over 
        # vertical separators as well
        K *= 1.25 
    return K


def v_Sounders_Brown(K, rhol, rhog):
    r'''Calculates the maximum allowable vapor velocity in a two-phase 
    separator to permit separation between entrained droplets and the gas
    using an empirical `K` factor, named after Sounders and Brown [1]_.
    This is a simplifying expression for terminal velocity and drag on 
    particles.
    
    .. math::
        v_{max} =  K_{SB} \sqrt{\frac{\rho_l-\rho_g}{\rho_g}}
        
    Parameters
    ----------
    K : float
        Sounders Brown `K` factor for two-phase separator design, [m/s]
    rhol : float
        Density of liquid phase [kg/m^3]
    rhog : float
        Density of gas phase [kg/m^3]

    Returns
    -------
    v_max : float
        Maximum allowable vapor velocity in a two-phase separator to permit 
        separation between entrained droplets and the gas, [m/s]

    Notes
    -----
    The Sounders Brown K factor is related to the terminal velocity as shown in 
    the following expression.
    
    .. math::
        v_{term} = v_{max} = \sqrt{\frac{4 g d_p (\rho_p-\rho_f)}{3 C_D \rho_f }}
        
        v_{term} = \sqrt{\frac{(\rho_p-\rho_f)}{\rho_f}} \sqrt{\frac{4 g d_p}{3 C_D}}
        
        v_{term} = K_{SB} \sqrt{\frac{4 g d_p}{3 C_D}}
        
    Note this form corresponds to the Newton's law range (Re > 500), but in 
    reality droplets are normally in the intermediate or Stoke's law region 
    [2]_. For this reason using the drag coefficient expression directly is 
    cleaner, but identical results can be found with the Sounders Brown 
    equation.

    Examples
    --------
    >>> v_Sounders_Brown(K=0.08, rhol=985.4, rhog=1.3)
    2.2010906387516167

    References
    ----------
    .. [1] Souders, Mott., and George Granger. Brown. "Design of Fractionating 
       Columns I. Entrainment and Capacity." Industrial & Engineering Chemistry
       26, no. 1 (January 1, 1934): 98-103. https://doi.org/10.1021/ie50289a025.
    .. [2] Vasude, Gael D. Ulrich and Palligarnai T. Chemical Engineering 
       Process Design and Economics : A Practical Guide. 2nd edition. Durham, 
       N.H: Process Publishing, 2004.
    '''
    return K*((rhol - rhog)/rhog)**0.5


def K_Sounders_Brown_theoretical(D, Cd, g=g):
    r'''Converts a known drag coefficient into a Sounders-Brown `K` factor
    for two-phase separator design. This factor is the traditional way for
    separator diameters to be obtained although it is unnecessary and the
    theoretical drag coefficient method can be used instead.
    
    .. math::
        K_{SB} = \sqrt{\frac{(\rho_p-\rho_f)}{\rho_f}} 
        = \sqrt{\frac{4 g d_p}{3 C_D}}
        
    Parameters
    ----------
    D : float
        Design diameter of the droplets, [m]
    Cd : float
        Drag coefficient [-]
    g : float, optional
        Acceleration due to gravity, [m/s^2]

    Returns
    -------
    K : float
        Sounders Brown `K` factor for two-phase separator design, [m/s]

    Notes
    -----
    Drag coefficient is a function of velocity; so iteration is needed to 
    obtain the most correct answer. The following example shows the use of 
    iteration to obtain the final velocity:
    
    >>> from fluids import *
    >>> V = 2.0 
    >>> D = 150E-6
    >>> rho = 1.3
    >>> rhol = 700.
    >>> mu = 1E-5
    >>> for i in range(10):
    ...     Re = Reynolds(V=V, rho=rho, mu=mu, D=D)
    ...     Cd = drag_sphere(Re)
    ...     K = K_Sounders_Brown_theoretical(D=D, Cd=Cd)
    ...     V = v_Sounders_Brown(K, rhol=rhol, rhog=rho)
    ...     print(V)
    0.760933074177
    0.562429393401
    0.507328950507
    0.489571420955
    0.483560219469
    0.481490760336
    0.480774149346
    0.480525499591
    0.480439162498
    0.480409176902

    The use of Sounders-Brown constants can be replaced as follows (the 
    v_terminal method includes its own solver for terminal velocity):
        
    >>> from fluids.drag import v_terminal
    >>> v_terminal(D=D, rhop=rhol, rho=rho, mu=mu)
    0.4803932186998833

    Examples
    --------    
    >>> K_Sounders_Brown_theoretical(D=150E-6, Cd=0.5)
    0.06263114241333939
     
    References
    ----------
    .. [1] Svrcek, W. Y., and W. D. Monnery. "Design Two-Phase Separators 
       within the Right Limits" Chemical Engineering Progress, (October 1, 
       1993): 53-60.
    '''
    return (4.0*g*D/(3.0*Cd))**0.5