#!/usr/bin/env python
"""
VIC $CASE.run command line interface
"""
# Note:  this is not intended to be a permant fixture.  Most users will need to
#     edit this based on run/machine/driver specifications.
import os.path
import sys

# add scripts dir to path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                os.pardir))

if __name__ == "__main__":
    from case_utils.case_tools import run

    casedir = os.path.split(os.path.abspath(__file__))[0]
    casename = os.path.split(casedir)[-1]
    run('{0}_global_param.txt'.format(casename), 'logs')
