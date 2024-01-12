# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:20:37 2024

@author: mbmad
"""
import numpy as np
import statistics as sts

def baseline(sweep,baseline):
    base = np.average(baseline.filt(sweep))
    sweep = np.subtract(sweep, base)
    return sweep, int(base)

def detectEvents(sweep, threshold: int = 0, minlength : int = 0, prominence = None, direction : int = 1):
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
    binnedvalues = []
    if binning == 0: binnedvalues.append(func(values))
    else: binnedvalues = [func(x) for x in zip(*[iter(values)] * binning)]
    return binnedvalues