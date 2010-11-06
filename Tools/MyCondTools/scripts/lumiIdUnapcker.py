#!/usr/bin/env python
from optparse import OptionParser, Option, OptionValueError


def unpackLumiid(lumiid):
    kLowMask = 0XFFFFFFFF
    run = lumiid >> 32
    lumi = lumiid & kLowMask
    return (run, lumi)



def main():
    parser = OptionParser()

#    parser.add_option(("-c", "--scenario", dest="scenario",
#                      help="GT scenario: ideal - mc - startup - data - craft09",
#                      type="str", metavar="<scenario>",action="append")

    (options, args) = parser.parse_args()

    for lumiid in args:
        runAndLumi = unpackLumiid(int(lumiid))
        print "lumiid: " + str(lumiid) + " -> run:lumi =  " + str(runAndLumi[0]) + ":" +  str(runAndLumi[1])
    


if __name__     ==  "__main__":
    main()

