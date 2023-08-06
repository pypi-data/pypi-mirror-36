
"""PURPOSE: select map(s) from an organized map pool."""

from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

import argparse

from sc2maptool.__version__ import __version__
from sc2maptool import constants as c
from sc2maptool.functions import selectMap, filterMapAttrs, filterMapNames


################################################################################
def optionsParser(passedParser=None):
    if passedParser == None:
        parser = argparse.ArgumentParser(
           #usage="python %s"%__file__,
            description=__doc__,
            epilog="version: %s"%__version__)
    else:
        parser = passedParser
    if not passedParser:
        actionOpt = parser.add_argument_group('Main routine behavior indicating information to provide')
        actionOpt.add_argument("--list"     , default=None, action="store_true", help="Display all known maps by category.")
        actionOpt.add_argument("--details"  , default=None, action="store_true", help="show details of each mapname.")
        actionOpt.add_argument("--path"     , default=None, action="store_true", help="provide the absolute path to the file.")
    functnOpt = parser.add_argument_group('Map Selection operation parameters')
    functnOpt.add_argument(    "--mapname"  , default=""                       , help="the (sub)name of the specific map to load.")
    functnOpt.add_argument(    "--exclude"  ,               action="store_true", help="exclude maps with names specified by --mapname.")
    if not passedParser:
        functnOpt.add_argument("--best"     ,               action="store_true", help="match maps that are closer with --mapname")
    matchOptn = parser.add_argument_group('Map record match criteria')
    matchOptn.add_argument(    "--ladder"   , default=None, type=bool          , help="ladder must be selected (True) or ignored.", metavar="BOOL")
    matchOptn.add_argument(    "--combat"   , default=None, type=bool          , help="combat maps must be selected (True) or ignored.", metavar="BOOL")
    matchOptn.add_argument(    "--economy"  , default=None, type=bool          , help="economy maps must be selected (True) or ignored.", metavar="BOOL")
    matchOptn.add_argument(    "--scenario" , default=None, type=bool          , help="single-player games with a specific objective to achieve must be selected (True) or ignored.", metavar="BOOL")
    matchOptn.add_argument(    "--misc"     , default=None, type=bool          , help="misc maps must be seleced (True) or ignored.", metavar="BOOL")
    matchOptn.add_argument(    "--test"     , default=None, type=bool          , help="test maps must be seleced (True) or ignored.", metavar="BOOL")
    matchOptn.add_argument(    "--year"     , default=None, type=int           , help="the calendar year the ladder season occurred.", metavar="INT")
    matchOptn.add_argument(    "--season"   , default=None, type=int, choices=[1, 2, 3, 4]
                                                                               , help="the specific ladder season within a calendar year.")
    matchOptn.add_argument(    "--mode"     , default=None, choices=["1v1", "2v2", "3v3", "4v4"]
                                                                               , help="the official ladder category to play.")
    return parser


################################################################################
def getSelectionParams(options):
    return {k:v for k,v in options._get_kwargs()\
        if v!=None and k in c.INCLUDED_KEYS}


################################################################################
def main(): # mini/unit test
    """
    PURPOSE: command-line interface for map information
    """
    options = optionsParser().parse_args()
    params = getSelectionParams(options)
    if options.list or options.details:
        specifiedMaps = filterMapNames(
            options.mapname,
            records = filterMapAttrs(**params),
            excludeRegex=options.exclude,
            closestMatch=options.best
        )
        if specifiedMaps:
            for v in specifiedMaps:
                if options.details: v.display()
                else:               print(v)
            print("Found %d maps that match given criteria."%(len(specifiedMaps)))
        else:
            print("No matching maps found.")
    else:
        try:
            specifiedMaps = selectMap(
                options.mapname,
                excludeName =options.exclude,
                closestMatch=options.best,
                **params)
        except Exception as e:
            specifiedMaps = []
            print("No matching maps found: %s"%e)
        if not isinstance(specifiedMaps, list):
            specifiedMaps = [specifiedMaps]
        for m in specifiedMaps:
            if options.path:    print(m.path)
            else:               print(m.name)

