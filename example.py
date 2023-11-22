# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:37:42 2023

@author: mbmad
"""

import pincer
import pincer.analysis_custom.cracm

mydata = pincer.CellDex(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data')
mydata.import_formattedexcel('celldex_30min_1mgkg_psilo_inj_11.21.23.xlsx')

analysis = pincer.AnalysisManager()
ap1 = analysis.get('CurrentInducedAP')
cracm = analysis.get('CRACM')
rheo = analysis.get('Rheoramp')
check = analysis.get('CheckSealStep')

mydata.queue_analysis(1, cracm)

mydata.process()

