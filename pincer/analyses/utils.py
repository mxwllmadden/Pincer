# -*- coding: utf-8 -*-
"""
Utility functions for pincer analyses
"""
import numpy as np
import statistics as sts
from pincer import ROI
import scipy.optimize

def baseline(sweep,baseline):
    """
    Simple baselineing function for sweeps.

    Parameters
    ----------
    sweep : np.array
        1D numpy array of a single ephys data sweep.
    baseline : np.array
        1D numpy array of a baseline region of an ephy sweep.

    Returns
    -------
    np.array
        new baselined sweep.
    int
        the average value of the baseline region

    """
    base = np.average(baseline.filt(sweep))
    sweep = np.subtract(sweep, base)
    return sweep, int(base)

def detectEvents(sweep, threshold: int = 0, minlength : int = 0, prominence : int = None, direction : int = 1):
    """
    Event detection function. Vital for action potential detection and similar
    processes.

    Parameters
    ----------
    sweep : np.array
        Sweep to be analyzed. 1D numpy array.
    threshold : int, optional
        Threshold value, events must cross this threshold to be counted.
        The default is 0.
    minlength : int, optional
        Minimum number of datapoints that the event must exceed threshold to
        be counted.
        The default is 0.
    prominence : int, optional
        An event peak must descend by this much on either side to be counted.
        The default is None.
    direction : int, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    events = []
    sweep = sweep * direction
    #detect every region where
    regions = reglabel(sweep>=threshold)
    eventcount = np.amax(regions)
    for i in range(int(eventcount)):
        #ensure region is equal or larger than minlength
        if np.count_nonzero(regions==(i+1)) >= minlength:
            #index of maximum value within region of interest
            evindex = np.argmax(sweep[regions==(i+1)])
            evindex = evindex + np.min(np.where(regions==(i+1)))
            events.append(evindex)
    #filter for prominent events only
    if prominence != None:
        events = _prominencefilter(sweep, events, prominence)
    return tuple(events)

def _prominencefilter(sweep,events,prominence):
    """
    Internally accessed function. Used by detectEvents to perform prominence 
    filtering.

    Parameters
    ----------
    sweep : np.array
        1D numpy array of a single sweep.
    events : list
        List of events to be filtered.
    prominence : int
        Required prominence.

    Returns
    -------
    filt_events : list
        List of events, filtered to only those with required prominence.

    """
    filt_events = []
    ready = True
    for i in range(len(events)):
        #get left and right events
        if i == 0: l_event = 0
        else: l_event = events[i-1]
        if i+1 == len(events): r_event = len(sweep)
        else: r_event = events[i+1]
        
        l_prom = sweep[events[i]] - np.min(sweep[l_event:events[i]])
        r_prom = sweep[events[i]] - np.min(sweep[events[i]:r_event])
        prom = min([l_prom, r_prom])
        
        if prom >= prominence:
            filt_events.append(events[i])
        else:
            ready = False
    if ready == False:
        filt_events = _prominencefilter(sweep, filt_events, prominence)
    return filt_events
    

def reglabel(sweep):
    """
    Utility function used by detectEvents. Takes a boolean numpy array and returns
    labeled regions by way of a 1D numpy array of the same size where False is
    replaced by 0, and True values are replaced by positive integers corresponding
    to the region number.

    Parameters
    ----------
    sweep : np.array
        1D boolean array.

    Returns
    -------
    sweepout : np.array
        1D integer array.

    """
    assert isinstance(sweep, np.ndarray) and sweep.ndim == 1, 'sweep is not a 1-d numpy array'
    assert sweep.dtype == bool, 'sweep dtype is not boolean'
    count = 0
    state = False
    sweepout = np.empty(len(sweep))
    for x in range(len(sweep)):
        if sweep[x] == True and state == False:
            count += 1
            state = True
            sweepout[x] = count
        if sweep[x] == False:
            state = False
            sweepout[x] = 0
        if sweep[x] == True and state == True:
            sweepout[x] = count
    return sweepout

def binning(values : list, binning, func):
    """
    Function for performing binning operations across results data. Bins a list
    into sublists of size 'binning' then inputs those list values into a user
    defined function. List values that do not fit into a bin are discarded.

    Parameters
    ----------
    values : list
        list of values to bin.
    binning : TYPE
        number of values to place in each bin.
    func : TYPE
        function to apply to each bin.

    Returns
    -------
    binnedvalues : list
        List of binned values.

    """
    binnedvalues = []
    if binning == 0: binnedvalues.append(func(values))
    else: binnedvalues = [func(x) for x in zip(*[iter(values)] * binning)]
    return binnedvalues

def confirmROI(value):
    """
    Simple utility function to confirm if an input is an ROI. If input is not ROI or None
    and is compatible with the ROI function, it will attempt to create an ROI by assuming
    the input is in milliseconds. This function also removes the need for an
    excessive litany of assert statments relating to ROI in each analysis.

    Parameters
    ----------
    value : TYPE
        Value to check.

    Returns
    -------
    None or ROI
        Successfully created ROI, original ROI, or None.

    """
    if type(value) == ROI:
        return value
    else:
        assert type(value) == tuple, 'input must be tuple, None, or ROI'
        assert len(value) == 2, 'tuple must have length 2'
        assert all(type(i) == int for i in value)
        return ROI(value)


