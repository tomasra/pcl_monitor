#!/usr/bin/env python

######################################################################
## File: misc.py
##
## Just useful stuff that didn't fit anywhere else.
##
######################################################################

import sys

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT import gStyle
from ROOT import TH1

import pdb
try:
    import debug_hook
except ImportError:
    pass

######################################################################

def DeUnicodeJSONKeys(dict_in):
    """Convert the unicode keys to plain strings for simplicity."""
    dict_out = {}
    for (key, val) in dict_in.iteritems():
        key_new = key.encode("utf-8")
        dict_out[key_new] = val

    return dict_out

######################################################################

def IntifyJSONKeys(dict_in):
    """Convert the unicode keys to integers for simplicity."""
    dict_out = {}
    for (key, val) in dict_in.iteritems():
        key_new = int(key)
        dict_out[key_new] = val

    return dict_out

######################################################################

def SetupROOT(batch=True):
    """Some useful ROOT settings not to be forgotten."""

    gROOT.SetBatch(batch)
    gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")

    gROOT.SetStyle("Plain")
    gStyle.SetOptStat("euo")
    gStyle.SetOptFit(111)
    gStyle.SetFuncWidth(1)
    gStyle.SetMarkerStyle(2)

    TH1.SetDefaultSumw2(True)

######################################################################

def LoadMatplotlib():
    """See if we can find and import matplotlib."""

    print "Loading matplotlib"

    matplotlib_loaded = False
    try:
        import matplotlib
        from matplotlib import pyplot as plt
        matplotlib.rcParams["legend.numpoints"] = 1
        matplotlib.rcParams["legend.fontsize"] = "medium"
        matplotlib.rcParams["text.usetex"] = True
        matplotlib.rcParams["text.latex.preamble"] = "\usepackage{amsmath}"
        matplotlib.rcParams["savefig.dpi"] = 300
        matplotlib_loaded = True
        # The following makes the (now local) imports global.
        # (I know, ugly, and probably only works in CPython.)
        sys._getframe(1).f_globals.update(locals())
    except ImportError:
        print "Could not find matplotib"

    return matplotlib_loaded

######################################################################
