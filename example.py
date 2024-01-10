# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:37:42 2023

@author: mbmad
"""

import pincer
import pincer.analysis_custom.cracm

mydata = pincer.CellDex(r'C:\Users\mbmad\OneDrive - University of Maryland School of Medicine\Documents\MATHURLAB DATA AND PROJECTS\Patch Data Archive\Data')
mydata.import_formattedexcel('celldex_24hr_1mgkg_psilo_inj.xlsx')

analysis = pincer.AnalysisManager()
ap1 = analysis.get('CurrentInducedAP')
cracm = analysis.get('CRACM')
rheo = analysis.get('Rheoramp')
check = analysis.get('CheckSealStep')

mydata.queue_analysis(1, cracm)
mydata.queue_analysis(0, ap1)
mydata.queue_analysis(2, rheo)
mydata.queue_analysis(9, check)

tname = ['100%','80%','60%','40%','20%','0%']
idents = [[x, 'Action Potentials per Light Pulse'] for x in tname]
mydata.queue_secondary_operation('Average APs/LP',idents)
idents = [[x, 'Area Under the Curve UNITS'] for x in tname]
mydata.queue_secondary_operation('Average Area Under the Curve UNITS',idents)

mydata.process(report = True)

mydata.export_formattedexcel(r'celldex_postprocess_test.xlsx')