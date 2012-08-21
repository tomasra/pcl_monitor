######################################################################
## File: run_and_fill_map_tools.py
##
## Just some tools and tricks.
##
######################################################################

import os
import sys
import json

from misc import IntifyJSONKeys

import pdb
try:
    import debug_hook
except ImportError:
    pass

######################################################################

all_years = [2011, 2012]

######################################################################

#def DataPath():
#
#    cmssw_base_path = os.getenv("CMSSW_BASE")
#    module_path_pieces = ["src", "LumiStudies", "LumiUtils", "data"]
#    data_path = cmssw_base_path
#    for i in module_path_pieces:
#        data_path = os.path.join(data_path, i)
#
#    # End of DataPath().
#    return data_path

def DataPath():

    cmssw_base_path = os.getenv("CMSSW_BASE")
    module_path_pieces = ["src", "MyAnalysis", "ZLumiStudy", "test", "FillingScheme", "data"]
    data_path = cmssw_base_path
    for i in module_path_pieces:
        data_path = os.path.join(data_path, i)

    # End of DataPath().
    return data_path

######################################################################

def LoadFillToRunMap(years=all_years):

    run_to_fill_map = LoadRunToFillMap(years)
    fill_to_run_map = {}
    for (run_number, fill_number) in run_to_fill_map.iteritems():
        try:
            fill_to_run_map[fill_number].append(run_number)
        except KeyError:
            fill_to_run_map[fill_number] = [run_number]

    # End of LoadFillToRunMap().
    return fill_to_run_map

######################################################################

def LoadRunToFillMap(years=all_years):

    try:
        len(years)
    except TypeError:
        years = [years]

    run_to_fill_map = {}
    for year in years:
        run_to_fill_map.update(_LoadRunToFillMap(year))

    # End of LoadRunToFillMap().
    return run_to_fill_map

######################################################################

def _LoadRunToFillMap(year):

    in_file_path = DataPath()
    in_file_name = "run_to_fill_map_%d.json" % year
    in_file_full = os.path.join(in_file_path, in_file_name)

    print "Reading run-to-fill map for %d from %s" % \
          (year, in_file_full)
    run_to_fill_map = None
    try:
        in_file = open(in_file_full, "r")
        run_to_fill_map = json.load(in_file)
        in_file.close()
    except IOError, err:
        print >> sys.stderr, "ERROR Could not read from file %s" % \
              in_file_full
        sys.exit(1)

    run_to_fill_map = IntifyJSONKeys(run_to_fill_map)

    # End of _LoadRunToFillMap()
    return run_to_fill_map

######################################################################

def LoadFillToSchemeMap(years=all_years):

    try:
        len(years)
    except TypeError:
        years = [years]

    fill_to_scheme_map = {}
    for year in years:
        fill_to_scheme_map.update(_LoadFillToSchemeMap(year))

    # End of LoadFillToSchemeMap()
    return fill_to_scheme_map

######################################################################

def _LoadFillToSchemeMap(year):

    in_file_path = DataPath()
    in_file_name = "fill_to_scheme_map_%d.json" % year
    in_file_full = os.path.join(in_file_path, in_file_name)

    print "Reading fill-to-scheme map for %d from %s" % \
          (year, in_file_full)
    fill_to_scheme_map = None
    try:
        in_file = open(in_file_full, "r")
        fill_to_scheme_map = json.load(in_file)
        in_file.close()
    except IOError, err:
        print >> sys.stderr, "ERROR Could not read from file %s" % \
              in_file_full
        sys.exit(1)

    fill_to_scheme_map = IntifyJSONKeys(fill_to_scheme_map)

    # End of _LoadFillToSchemeMap()
    return fill_to_scheme_map

######################################################################

def LoadRunToSchemeMap(years=all_years):

    # Hmmmm.... Not sure this is cool or nasty.
    try:
        len(years)
    except TypeError:
        years = [years]

    run_to_scheme_map  = {}

    for year in years:
        run_to_fill_map = LoadRunToFillMap(year)
        fill_to_scheme_map = LoadFillToSchemeMap(year)

        for (run, fill) in run_to_fill_map.iteritems():
            run_to_scheme_map[run] = fill_to_scheme_map[fill]

    # End of LoadRunToSchemeMap().
    return run_to_scheme_map

######################################################################
