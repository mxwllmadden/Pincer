# -*- coding: utf-8 -*-
"""
Main Pincer Module
Contains primary Pincer classes ROI and Pincer.

Maxwell Madden
"""

import pandas, numpy as np
from pathlib import Path, PurePath
from pincer.abfHelper import PincerABF

class ROI():
    """
    Defines a Range of Interest (ROI) within an ephys recording.
    
    Handles automatic unit conversion given the variable sampling rates contained in 
    ephys recordings. Defaults to ms units if not specified.
    """
    _defaultunits = {'us': 1,'ms':1000,'s':1000000,'sec':1000000,'min':60000000}
    """
    _defaultunits is a class variable containing a list of units as well as their
    conversion to microseconds. It is NOT recommended to edit the class variable
    to add new units.
    """
    def __init__(self,region : tuple,unit : str = 'ms'):
        """
        Create an ROI object that describes a range in an ephys trace.

        Parameters
        ----------
        region : tuple
            A tuple, or tuple of tuples, each containing two integers defining
            the start and end of the ROI. (X,Y) defines a region from X to Y, 
            including X and excluding Y. ((X1,Y1),(X2,Y2)) defines a two part
            region, from X1 to Y1 and X2 to Y2. The region always including the
            sample X and counts up to Y, excluding Y.
        unit : str, optional
            String specifying the units of the ROI from the _defaultunits class
            variable dictionary. The default is 'ms'.

        Returns
        -------
        Pincer.ROI object.

        """
        self._units = self._defaultunits
        assert unit in self._units.keys(), 'invalid unit, use one of: '+', '.join(list(self._units.keys()))
        assert type(region) == tuple or type(region) == list, 'regions must be defined as a tuple or list of tuples'
        if type(region) == tuple: region = [region]
        
        assert all([type(x) == tuple for x in region]), 'ranges must be tuples'
        for i in region:
            assert all([type(x) == int for x in i]), 'start and end of range must be int'
            assert len(i) == 2, 'ranges may only be defined as (start,end)'
            
        self.region = region
        self._mergeranges()
        self.unit = unit
        
    def filt(self,trace : np.ndarray):
        """
        Filters an ephys trace to include only samples from the ROI. DO NOT USE
        UNLESS ROI UNITS HAVE BEEN CONVERTED TO SAMPLES.

        Parameters
        ----------
        trace : np.ndarray
            1 dimensional numpy array containing ephys trace samples.

        Returns
        -------
        np.ndarray
            1 dimensional numpy array containing ephys trace samples, filtered
            to include only samples within ROI.

        """
        assert self.unit == 'samples', 'ROI must be in sample units'
        assert type(trace) == np.ndarray, 'trace must be numpy.ndarray'
        arrays = [trace[s:e] for s, e in self.region]
        return np.concatenate(arrays)
        
    def samplcnv(self,hz : int):
        """
        Convert ROI to sample units

        Parameters
        ----------
        hz : int
            Sampling rate in hz. Can be directly retreived from abf file header.

        Returns
        -------
        Self
            Optionally returns self, can be useful when attempting to write
            single line statements.

        """
        assert hz < 100000, 'ROI cannot handle sample rates higher than 100khz'
        self._units['samples'] = int(1/(hz/1000000))
        self.convertunit('samples')
        return self
        
    def _mergeranges(self):
        """
        Internally accessed method. Used to merge overlapping ranges when they
        occur.

        Returns
        -------
        None.

        """
        result = []
        for i in sorted(self.region):
            result = result or [i]
            if i[0] >= result[-1][1]:
                result.append(i)
            else:
                old = result[-1]
                result[-1] = (old[0], max(old[1], i[1]))
        self.region = result
    
    def convertunit(self,unit : str):
        """
        Convert units between internally defined unit options. Be careful when
        converting to larger units, as ROI may round units to preserve integer
        data type for defining range.

        Parameters
        ----------
        unit : string
            Unit from internal unit dictionary (_units).

        Returns
        -------
        None.

        """
        assert unit in self._units.keys(), 'invalid unit, use one of: '+', '.join(list(self._units.keys())) 
        self.region = [tuple([i*self._units[self.unit]//self._units[unit] for i in y]) for y in self.region]
        self.unit = unit
        
    def _makefriendlywith(self,new):
        """
        Internally accessed method. Changes units between ROI to match. Rounding
        errors may occur if ranges are defined by non-standard units.

        Parameters
        ----------
        new : ROI
            Second ROI object to make unit compatible.

        Returns
        -------
        None.

        """
        newunit = min(self._units[self.unit],new._units[new.unit])
        x = self._units | new._units
        lookup = {v:k for k,v in x.items()}
        if self._units[self.unit] != newunit: self.convertunit(lookup[newunit])
        if new._units[new.unit] != newunit: new.convertunit(lookup[newunit])
    
    def __add__(self, new):
        """
        Magic method to allow addition of ROI objects. Produces a region equal to
        the union of both ROIs.

        Parameters
        ----------
        new : ROI
            ROI object to be added.

        Returns
        -------
        ROI
            New ROI object containing the union of the regions defined in the
            input ROIs.

        """
        self._makefriendlywith(new)
        result = self.region + new.region
        return ROI(result, unit = self.unit)
    
    def __repr__(self):
        return 'Pincer Range of Interest (ROI) including ' + ' '.join(str(x) for x in self.region).replace('(','[') + ' in unit (' + self.unit + ')'    

class Pincer():
    """
    Primary Pincer Class.
    
    Takes imported tabular array of file names, queues analysis objects, then performs
    appropriate analysis across all files and collects the results in tabular
    format.
    """
    def __init__(self,source : str,padfilename : int = 3):
        """
        Generate a Pincer object with specific paramaters

        Parameters
        ----------
        source : str
            String representing a filepath to the directory containing all .abf
            ephys data files.
        padfilename : int, optional
            Number of integers expected in the second portion of the unique 
            filename generated by clampex. The default is 3.

        Returns
        -------
        New Pincer object.

        """
        # Setup dataframes
        self.source = Path(source)
        self._initiateDataFrames()
        self.padfilename = padfilename
        
        # Setup analysis, secondary measures, and secondary frames.
        self.analysis_queue = {}
        self.secondary_ops_queue = []
        self.comparisons = []
        
    def _initiateDataFrames(self):
        """
        Internally accessed function. Sets up the dataframes for import.

        Returns
        -------
        None.

        """
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

    def import_formattedexcel(self,filepath : str):
        """
        Imports tabular trace, cell, and animal data from a properly formatted
        excel file.

        Parameters
        ----------
        filepath : str
            filepath of imported excel file.

        Returns
        -------
        None.

        """
        xls = pandas.ExcelFile(filepath)
        self.cellLabels = pandas.read_excel(xls,'CellLabels',header = 0, index_col=[0,1,2],dtype= str)
        self.traceIndex = pandas.read_excel(xls, 'TraceIndex',header=[0,1],index_col=[0,1,2],dtype= str)
        self.animalLabels = pandas.read_excel(xls, 'AnimalLabels',header=0,index_col=[0],dtype= str)
                            
    def export_formattedexcel(self,filepath, *kwargs):
        """
        Exports all tabular data to a properly formatted excel file.

        Parameters
        ----------
        filepath : str
            filepath of exported excel file.
        *kwargs : TYPE
            Keword arguments to be passed to the Pandas ExcelWriter.

        Returns
        -------
        None.

        """
        expfile = pandas.ExcelWriter(filepath, *kwargs)
        self.cellLabels.to_excel(expfile, sheet_name = 'Celllabels', engine='xlswriter')
        self.animalLabels.to_excel(expfile, sheet_name = 'AnimalLabels', engine='xlswriter')
        self.traceIndex.to_excel(expfile, sheet_name='TraceIndex', engine='xlswriter')
        self.results.to_excel(expfile, sheet_name='Results', engine='xlswriter')
        self.animalresults.to_excel(expfile, sheet_name= 'Results by Animal', engine='xlswriter')
        expfile.close()
        del expfile 
    
    def queue_analysis(self,index : int,analysis):
        """
        Add an analysis object to the queue and specify the appropriate index.

        Parameters
        ----------
        index : int
            Integer code contained in the tabular tracedata which can be used
            to identify the correct analysis.
        analysis : TYPE
            An analysis object, see pincer.analysis_base.PincerAnalysis
            The object must contain a 'run' method, which will be passed the
            abf file for analysis during processing.

        Returns
        -------
        None.

        """
        self.analysis_queue[index] = analysis
    
    def queue_secondary_measure(self, outputname : str = 'example', resultsidentifiers : list = [], function = np.mean):
        """
        Queue a secondary measure. Secondary measures take results and apply
        a function across them, this allows the generation of outputs that
        integrate features from multiple .abf files.
        
        Parameters
        ----------
        outputname : str, optional
            Name of the secondary measure. The default is 'example'.
        resultsidentifiers : list, optional
            List of results names, used to filter results data to include only
            the desired inputs for the secondary operations function. 
            The default is [].
        function : TYPE, optional
            A function that will be applied across all filtered analysis results.
            The default is np.mean, which will take the mean of all measures
            specified by resultsidentifiers.

        Returns
        -------
        None.

        """
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
        return True
        """Needs to be written!"""
        
        
    def process(self, report : bool = False, check : bool = False):
        """
        Apply all analyses, secondary operations, and comparisons and collect
        those outputs in tabular format.

        Parameters
        ----------
        report : bool, optional
            Turn on verbose reporting to the CLI. The default is False.
        check : bool, optional
            Run the check function across all files prior to processing. A failed
            check DOES NOT prevent processing. The default is False.

        Returns
        -------
        None.

        """
        go = True
        if check == True:
            go = self.check()
        if go == False:
            print('process aborted due to failed check')
        else:
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
                            file = self.cmbABFnm(index[0], code)
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
            """for op in self.secondary_ops_queue:
                features = [self.results[*i] for i in op['inputIDs']]
                featureframe = pandas.concat(features,axis = 1)
                self.results['SecondaryOutputs',op['outputname']] = featureframe.apply(op['func'], axis = 1)"""
            if report == True: print('Calculating Animalwise Measures!')
            self.animalresults = self.results.groupby(level=0,axis=0).mean()
            print('Done!')
            
    def checkfiles(self):
        pass
    
    def _run_analysis(self):
        pass
    
    def _iterate_func_over_analysis_index(self):
        pass
        
    def cmbABFnm(self,daycode,index):
        """
        Method to combine the 'daycode' portion of the filename, which is constant
        across all files within a given day, to the file index, which makes each
        filename unique. This method can be overwritten by the user to provide
        additional flexibility.
        
        The unique index is padded by zeroes to produce indexes of an expected
        length. This behavior can be disabled by setting the padfilename to zero
        in __init__.

        Parameters
        ----------
        daycode : str
            First portion of a given filename. The portion Clampex uses to indicate
            the date of recording in YYMDD format.
        index : str
            The portion of a filename that indicates the number of the recording
            within a given day, counts from 0.

        Returns
        -------
        str
            DESCRIPTION.

        """
        d = str(daycode)
        i = str(index)
        i = i.partition('.')[0]
        i = i.rjust(self.padfilename,'0')
        return d + i.zfill(self.padfilename) + '.abf'