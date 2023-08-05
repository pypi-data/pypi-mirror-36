#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 16:09:37 2018

@author: antony
"""

import os
import re
from abc import ABC, abstractmethod

LOC_REGEX = re.compile(r'(chr(?:[1-9][0-9]?|[XYM])):(\d+)-(\d+)')
SHORT_LOC_REGEX = re.compile(r'(chr(?:[1-9][0-9]?|[XYM])):(\d+)')



class Loc(object):
    def __init__(self, chr, start, end):
        self.__chr = chr
        self.__start = start
        self.__end = end
        
    @property
    def chr(self):
        return self.__chr
    
    @property
    def start(self):
        return self.__start
    
    @property
    def end(self):
        return self.__end
    
    def __str__(self):
        return '{}:{}-{}'.format(self.chr, self.start, self.end)
    

def is_loc_obj(l):
    """
    Tests whether a location is a tuple containing an str and
    two ints to represent a genomic position
    
    Parameters
    ----------
    l : str or tuple of (str, int, int)
        Location
    
    Returns
    -------
    bool
        True if location tuple.
    """
    
    return isinstance(l, Loc)


def is_loc(loc):
    """
    Returns true if string is a location ('chr1:1-2')
    """
    
    return LOC_REGEX.match(loc) is not None or SHORT_LOC_REGEX.match(loc) is not None

def parse_loc(loc):
    #print('args', loc)
    
    if is_loc_obj(loc):
        # already a location tuple, so return it
        return loc
    elif isinstance(loc, tuple):
        # multiple args mean a separate chr, start, and end
        return Loc(loc[0], loc[1], loc[2])
        # A string so parse it
    else:    
        # remove commas in numbers
        location = loc.replace(',', '')
        matcher = LOC_REGEX.match(location)
         
        if matcher is not None:
            chr = matcher.group(1)
            start = int(matcher.group(2))
            end = int(matcher.group(3))
        
            if end >= start:
                return Loc(chr, start, end)
            else:
                return Loc(chr, end, start)
        else:
            matcher = SHORT_LOC_REGEX.match(location)
            
            if matcher is not None:
                chr = matcher.group(1)
                start = int(matcher.group(2))
                
                return Loc(chr, start, start)
            else:
                return None
