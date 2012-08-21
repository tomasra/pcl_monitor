#!/usr/bin/env python

######################################################################
## File: constants.py
##
## Some useful constants used (mainly) in the pixel cluster luminosity
## code.
##
######################################################################

NUM_BX = 3564
FREQ_ORBIT = 11246.
SECONDS_PER_LS = 2 ** 18 / FREQ_ORBIT

##########

# The total pixel cluster cross section comes from a presentation Dan
# sent around at some point. They are based on the May 2011
# Van-der-Meer scan.

# Using all pixel clusters:
# XSEC_PIXEL_CLUSTER = 10.08e-28
# XSEC_PIXEL_CLUSTER_UNC = .17e-28

# Excluding the inner barrel layer.
XSEC_PIXEL_CLUSTER_2011 = 7.122e-28
XSEC_PIXEL_CLUSTER_UNC_2011 = .084e-28

##########

# BUG BUG BUG
# Scaled-up versions of 2011 for 2012. Scaled up by 2% based on
# Danek's estimates of the effect of the change from 3.5 to 4.0 TeV.
# BUG BUG BUG end

# Excluding the inner barrel layer.
factor = 1.02
XSEC_PIXEL_CLUSTER_2012 = factor * XSEC_PIXEL_CLUSTER_2011
XSEC_PIXEL_CLUSTER_UNC_2012 = factor * XSEC_PIXEL_CLUSTER_UNC_2011

##########

xsec_pixel_cluster = {
    2011 : (XSEC_PIXEL_CLUSTER_2011, XSEC_PIXEL_CLUSTER_UNC_2011),
    2012 : (XSEC_PIXEL_CLUSTER_2012, XSEC_PIXEL_CLUSTER_UNC_2012),
    }

######################################################################
