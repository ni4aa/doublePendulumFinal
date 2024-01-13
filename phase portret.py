import matplotlib.pyplot as plt
import numpy as np
from math import *

g = 9.8067


def d2x(m1, m2, l, phi, dphi):
    return -m2 * (g * cos(phi) * sin(phi) + l * sin(phi) * dphi**2) / (m2 * cos(phi)**2 - m2 - m1)


def d2phi(m1, m2, l, phi, dphi):
    return -((-g * m1 * sin(phi) - g * m2 * sin(phi) - l * m2 * cos(phi) * sin(phi) * dphi**2) / (l * (m2 * cos(phi)**2 - m2 - m1)))



