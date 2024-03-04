# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 12:43:50 2024

@author: mbmad
"""

import pincer
import pincer.analyses.cracm as cracm
from pincer.abfHelper import PincerABF as abf

baseline = pincer.ROI((0,200))
stimregions = (pincer.ROI((200,355)), pincer.ROI((355,410)), pincer.ROI((410,565)))


an_cracm = cracm.CRACM_Current_LightPulse(baseline,lightpulsespertrace=3, stimregions = stimregions)

print(an_cracm.run(abf('F:/Data/23817024.abf')))