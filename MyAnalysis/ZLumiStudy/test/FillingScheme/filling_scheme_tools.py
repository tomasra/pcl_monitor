######################################################################
## File: filling_scheme_tools.py
##
## Just some tools and tricks for handling LHC filling schemes.
##
######################################################################

import sys
import os
import re
import commands

from constants import NUM_BX
from run_and_fill_map_tools import LoadRunToFillMap
from run_and_fill_map_tools import LoadFillToSchemeMap

import pdb
try:
    import debug_hook
except ImportError:
    pass

######################################################################

# def rindex(list_in, value):
#     return len(list_in) - list_in[-1::-1].index(value) - 1

######################################################################

class LHCFillingScheme(object):

    def __init__(self, scheme_file_name):
        self.name = scheme_file_name.replace(".txt", "")

        try:
            scheme_file = open(scheme_file_name, "r")
            scheme_def_lines = scheme_file.readlines()
            scheme_file.close()
        except IOError:
            print >> sys.stderr, \
                  "ERROR Could not read filling scheme definition file"
            sys.exit(1)

        (self.beam1_pattern, self.beam2_pattern) = \
                             ParseFillingSchemeDef(scheme_def_lines)

        # DEBUG DEBUG DEBUG
        assert len(self.beam1_pattern) == len(self.beam2_pattern)
        # DEBUG DEBUG DEBUG end

        print "Found %d filled bunch crossings per beam" % \
              len(self.beam1_pattern)

        # Build the pattern of colliding bunches at CMS.
        set1 = set(self.beam1_pattern)
        set2 = set(self.beam2_pattern)
        self.active_bx_list = list(set1.intersection(set2))
        self.active_bx_list.sort()

        # DEBUG DEBUG DEBUG
        assert len(self.active_bx_list) == int(self.name.split("_")[2])
        # DEBUG DEBUG DEBUG end

        print "Found %d active bunch crossings for CMS" % len(self.active_bx_list)

        active_bx_pattern = NUM_BX * [0]
        for bx in self.active_bx_list:
            # NOTE: Shift down bx numbers (which start at 1) to array
            # indices.
            active_bx_pattern[bx - 1] = 1.
        self.active_bx_pattern = active_bx_pattern

    def num_bunches_per_beam(self):
        num_bunches = len(self.beam1_pattern)
        return num_bunches

    def num_active_crossings(self):
        num_active_bx = len(self.active_bx_list)
        return num_active_bx

    def filled_crossings(self, beam):
        crossings = None
        if beam == 1:
            crossings = self.beam1_pattern
        elif beam == 2:
            crossings = self.beam2_pattern
        else:
            assert False, "Impossible beam number: %d" % beam
        return crossings

    def last_active_crossing(self):
        bx = self.active_bx_list[-1]
        return bx

    # End of class LHCFillingScheme.

######################################################################

def ParseFillingSchemeDef(scheme_def_lines):
    """Parse contents of LPC filling scheme definition file."""

    # We'll be looking for lines that look like '# BEAM1 BEAM2 slots'
    # to find where the relevant data blocks start.
    regexp = re.compile("^# *BEAM([1,2]{1}) *BEAM([1,2]{1}) slots *$")

    beam_patterns = {1 : [], 2 : []}
    data_block = None
    processing_data_block = False

    for line in scheme_def_lines:

        line = line.strip()
        if not len(line):
            continue

        if line.startswith("#"):
            if processing_data_block:
                data_block = None
                processing_data_block = False
            match = regexp.match(line)
            if match:
                # Found the start of either the beam1 or the beam2
                # data block.
                # DEBUG DEBUG DEBUG
                assert set(match.groups()) == set(['1', '2'])
                # DEBUG DEBUG DEBUG end
                data_block = int(match.group(1))
            continue

        if not data_block:
            continue

        processing_data_block = True

        bx_nr = int(line.split()[0])
        beam_patterns[data_block].append(bx_nr)

    beam1_pattern = beam_patterns[1]
    beam2_pattern = beam_patterns[2]

    # DEBUG DEBUG DEBUG
    assert len(beam1_pattern) == len(beam2_pattern)
    # DEBUG DEBUG DEBUG end

    # End of ParseFillingSchemeDef().
    return (beam1_pattern, beam2_pattern)

######################################################################

def GetFillingScheme(**args):
    # Needs a run number, a fill number or a filling scheme name as
    # input.

    filling_scheme_name = None
    fill_number = None
    run_number = None

    if args.has_key("run_number"):
        run_number = args["run_number"]
        run_to_fill_map = LoadRunToFillMap()
        fill_number = run_to_fill_map[run_number]
        fill_to_scheme_map = LoadFillToSchemeMap()
        filling_scheme_name = fill_to_scheme_map[fill_number]
    elif args.has_key("fill_number"):
        fill_number = args["fill_number"]
        fill_to_scheme_map = LoadFillToSchemeMap()
        filling_scheme_name = fill_to_scheme_map[fill_number]
    elif args.has_key("filling_scheme_name"):
        filling_scheme_name = args["filling_scheme_name"]
    else:
        print >> sys.stderr, "ERROR Have to specify a run number, " \
              "a fill number or a filling scheme name"
        return None

    ##########

    #lpc_url = "http://lpc.web.cern.ch/lpc/documents/FillPatterns/"
    lpc_url = "http://lpc-afs.web.cern.ch/lpc-afs/FILLSCHEMES/"

    scheme_file_name = "%s.txt" % filling_scheme_name

    scheme_file_url = "%s/%s" % (lpc_url, scheme_file_name)

    ##########

    # Get the filling scheme text file.

    # First see if it is available locally, otherwise get it from the
    # LPC web site.
    if not os.path.isfile(scheme_file_name):
        print "Trying to get filling scheme file for '%s' " \
              "from the LPC web site" % filling_scheme_name
        cmd = "curl -f %s -o %s" % (scheme_file_url, scheme_file_name)
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            tmp = os.linesep.join([i for i in output.split(os.linesep) \
                                   if i.find("curl") > -1])
            print >> sys.stderr, \
                "ERROR Could not get filling scheme from LPC web site: '%s'" % \
                tmp
            sys.exit(1)
    else:
        print "Using locally stored filling scheme file for '%s'" % \
              filling_scheme_name

    ##########

    # Read and parse the filling scheme definition file and turn it
    # into a filling scheme object.
    filling_scheme = LHCFillingScheme(scheme_file_name)

    ##########

    # End of GetFillingScheme().
    return filling_scheme

######################################################################
