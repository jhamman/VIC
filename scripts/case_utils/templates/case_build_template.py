#!/usr/bin/env python
"""VIC $CASE.build command line interface"""
import os.path
import sys

casename = 'test0'

# add scripts dir to path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                os.pardir))

if __name__ == "__main__":
    from case_utils.case_tools import make, log_to_readme
    log_to_readme('{casename}.readme.md'.format(), 'Build Started')
    try:
        make('Build/Makefile', 'Build/logs')
        log_to_readme('{casename}.readme.md'.format(casename=casename),
                      'Build Completed')
    except RuntimeError:
        log_to_readme('{casename}.readme.md'.format(casename=casename),
                      'Build Failed')
