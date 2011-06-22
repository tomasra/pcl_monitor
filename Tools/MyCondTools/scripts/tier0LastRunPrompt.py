#!/usr/bin/env python

from Tools.MyCondTools.RunValues import *

if __name__ == "__main__":
    rv = RunValues()
    lastPromptRecoRun = rv.getLargestReleasedForPrompt("https://cmsweb.cern.ch/tier0/runs")
    print lastPromptRecoRun
