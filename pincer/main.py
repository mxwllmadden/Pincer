# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:49:00 2023

@author: mbmad
"""

import pandas, numpy as np
from pathlib import Path, PurePath
from pincer.analysis_base import AnalysisManager
from pincer.abfHelper import PincerABF
from pincer.analysis_base import StatsManager
import pincer.comparisons_stock

class CellDex():
    def __init__(self,source):
        # Setup dataframes
        self.source = Path(source)
        self._initiateDataFrames()
        
        # Setup analysis, secondary measures, and secondary frames.
        self.analysis_queue = {}
        self.secondary_ops_queue = []
        self.comparisons = []
        
    def _initiateDataFrames(self):
        rowmultiindex = pandas.MultiIndex(levels = [[],[],[]],
                                          codes = [[],[],[]],
                                          names = [u'Day',u'Slice',u'Cell'])
        colmultiindex = pandas.MultiIndex(levels = [[],[]],
                                          codes = [[],[]],
                                          names = [u'Trace',u'Output'])
        self.cellLabels = pandas.DataFrame()
        self.traceIndex = pandas.DataFrame()
        self.animalLabels = pandas.DataFrame()
        self.results = pandas.DataFrame(index=rowmultiindex, columns=colmultiindex)
        self.animalresults = pandas.DataFrame()

    def import_formattedexcel(self,filepath):
        xls = pandas.ExcelFile(filepath)
        self.cellLabels = pandas.read_excel(xls,'CellLabels',header = 0, index_col=[0,1,2],dtype= str)
        self.traceIndex = pandas.read_excel(xls, 'TraceIndex',header=[0,1],index_col=[0,1,2],dtype= str)
        self.animalLabels = pandas.read_excel(xls, 'AnimalLabels',header=0,index_col=[0],dtype= str)
                            
    def export_formattedexcel(self,filepath, *kwargs):
        expfile = pandas.ExcelWriter(filepath, *kwargs)
        self.cellLabels.to_excel(expfile, sheet_name = 'Celllabels', engine='xlswriter')
        self.animalLabels.to_excel(expfile, sheet_name = 'AnimalLabels', engine='xlswriter')
        self.traceIndex.to_excel(expfile, sheet_name='TraceIndex', engine='xlswriter')
        self.results.to_excel(expfile, sheet_name='Results', engine='xlswriter')
        self.animalresults.to_excel(expfile, sheet_name= 'Results by Animal', engine='xlswriter')
        expfile.close()
        del expfile 
    
    def queue_analysis(self,index,method):
        self.analysis_queue[index] = method
    
    def queue_secondary_measure(self, outputname = 'example', resultsidentifiers = [], function = np.mean):
        op = {}
        op['outputname'] = outputname
        op['inputIDs'] = resultsidentifiers
        op['func'] = function
        self.secondary_ops_queue.append(op)
        
    def check(self):
        """
        Process through all trace files, checking their
            Length
            Sampling Rate
            Number of Sweeps
            Epoch
            Source Protocol Name
            If trace exceeds expected bounds
        To see if different from other traces (minority groupings are reported)
        
        check WILL NOT catch bad data, only help identify where incorrect files
        have been entered.
        """
        pass
        """Needs to be written!"""
        
        
    def process(self, report = False, check = False):
        go = True
        if check == True:
            go = self.check()
        if go == True:
            print('This may take a while...')
            for analysis in self.analysis_queue.keys():
                if report == True: print('Performing '+ type(self.analysis_queue[analysis]).__name__ + 'analysis')
                for index, row in self.traceIndex[analysis].iterrows(): #Dataframe with only relevant analyses
                    #index is the index of the specific row, ROW is the series
                    for name, code in row.items():
                        #index is the cell index
                        #name is the name of the protocol
                        #code is the code for the recording
                        if str(code) != 'nan':
                            file = cmbABFnm(index[0], code)
                            if report == True: print('processing ',file)
                            filepath = PurePath(self.source, Path(file))
                            try:
                                abf = PincerABF(str(filepath))
                            except ValueError:
                                print("missing file:"+file)
                            else:
                                resultdict = self.analysis_queue[analysis].run(abf)
                                del abf
                                for result in resultdict.keys():
                                    self.results.loc[index,(name,result)] = resultdict[result]
            if report == True: print('Calculating Secondary Measures')
            for op in self.secondary_ops_queue:
                features = [self.results[*i] for i in op['inputIDs']]
                featureframe = pandas.concat(features,axis = 1)
                self.results['SecondaryOutputs',op['outputname']] = featureframe.apply(op['func'], axis = 1)
            if report == True: print('Calculating Animalwise Measures!')
            self.animalresults = self.results.groupby(level=0,axis=0).mean()
            print('Done!')
        else:
            print('Processing aborted due to reported failed check')
        
def cmbABFnm(daycode,index):
    d = str(daycode)
    i = str(index)
    i = i.partition('.')[0]
    i = i.rjust(3,'0')
    return d + i.zfill(3) + '.abf'