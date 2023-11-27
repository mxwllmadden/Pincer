# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:31:54 2023

@author: mbmad
"""
import numpy as np

def testmultiout(x : int):
    assert isinstance(x, np.ndarray)
    print(x)
    return 1

if __name__ == "__main__":
    x = np.array([1,2,3])
    testmultiout(x)
    x = 1
    testmultiout(x)

