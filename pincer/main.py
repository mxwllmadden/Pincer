# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:49:00 2023

@author: mbmad
"""

import pandas
from pathlib import Path, PurePath
from pincer.analysis_base import AnalysisManager
from pincer.abfHelper import PincerABF

class CellDex():
    def __init__(self,source):
        self.source = Path(source)
        self.analysis_queue = {}
        self._initiateDataFrames()
        
    def _initiateDataFrames(self):
        rowmultiindex = pandas.MultiIndex(levels = [[],[],[]],
                                          codes = [[],[],[]],
                                          names = [u'Day',u'Slice',u'Cell'])
        colmultiindex = pandas.MultiIndex(levels = [[],[]],
                                          codes = [[],[]],
                                          names = [u'Trace',u'Output'])
        
        self.CellLabels = pandas.DataFrame()
        self.TraceIndex = pandas.DataFrame()
        self.Results = pandas.DataFrame(index=rowmultiindex, columns=colmultiindex)

    def import_formattedexcel(self,filepath):
        xls = pandas.ExcelFile(filepath)
        self.CellLabels = pandas.read_excel(xls,'CellLabels',header = 0, index_col=[0,1,2])
        self.TraceIndex = pandas.read_excel(xls, 'TraceIndex',header=[0,1],index_col=[0,1,2])
    
    def queue_analysis(self,index,method):
        self.analysis_queue[index] = method
        
    def process(self):
        for analysis in self.analysis_queue.keys():
            for index, row in self.TraceIndex[analysis].iterrows(): #Dataframe with only relevant analyses
                #index is the index of the specific row, ROW is the series
                for name, code in row.items():
                    #index is the cell index
                    #name is the name of the protocol
                    #code is the code for the recording
                    file = cmbABFnm(index[0], code)
                    filepath = PurePath(self.source, Path(file))
                    abf = PincerABF(str(filepath))
                    resultdict = self.analysis_queue[analysis].run(abf)
                    for result in resultdict.keys():
                        self.Results.loc[index,(name,result)] = resultdict[result]
                    

def cmbABFnm(daycode,index):
    d = str(daycode)
    i = str(index)
    return d + i.zfill(3) + '.abf'