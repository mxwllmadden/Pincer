# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:31:54 2023

@author: mbmad
"""

import pyabf

x= pyabf.ABF(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data\23n17083.abf')

print(x.protocol)
print(x.headerHTML)

y = pyabf.ABF(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data\23n17083.abf', loadData=False)

def test(*args,bingo = 'bango',**kwargs):
    print(*args)
    print(kwargs)
    print(bingo)

test('hi','fuck',hello = 'fuck',bingo = 'hatata')

