#!/usr/bin/env python
from __future__ import print_function
from collections import namedtuple
import subprocess
import warnings
import sys
import os

_py3 = True if sys.version_info[0] >= 3 else False

version = namedtuple('git_version', ['full', 'short', 'tag'])
version.full = '5.0.0-Alpha Septeber 18, 2015'
version.short = '5.0.0-Alpha'
version.tag = 'VIC.5.0.0'

version_header_template = '''
/******************************************************************************
 * @section DESCRIPTION
 *
 * Header file for build time metadata
 *
 * @section LICENSE
 *
 * The Variable Infiltration Capacity (VIC) macroscale hydrological model
 * Copyright (C) 2014 The Land Surface Hydrology Group, Department of Civil
 * and Environmental Engineering, University of Washington.
 *
 * The VIC model is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *****************************************************************************/

#ifndef VIC_VERSION_H
#define VIC_VERSION_H

#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)

#define VERSION "{0}"
#define SHORT_VERSION "{1}"
#define GIT_TAG "{2}"

#define BUILD_DATE __DATE__
#define BUILD_TIME __TIME__

/* Get compiler metadata */
#if defined(__clang__)
/* Clang/LLVM. ---------------------------------------------- */
# define COMPILER "clang"
# define COMPILER_VERSION __clang_version__

#elif defined(__ICC) || defined(__INTEL_COMPILER)
/* Intel ICC/ICPC. ------------------------------------------ */
# define COMPILER "icc"
# define COMPILER_VERSION __version__

#elif defined(__GNUC__) || defined(__GNUG__)
/* GNU GCC/G++. --------------------------------------------- */
# define COMPILER "gcc"
# define COMPILER_VERSION STR(__GNUC__) "." STR(__GNUC_MINOR__) "." STR(__GNUC_PATCHLEVEL__)

#elif defined(__PGI)
/* Portland Group PGCC/PGCPP. ------------------------------- */
# define COMPILER "pgcc"
# define COMPILER_VERSION __PGIC__ __PGIC_MINOR __PGIC_PATCHLEVEL__

#elif defined(__SUNPRO_C) || defined(__SUNPRO_CC)
/* Oracle Solaris Studio. ----------------------------------- */
# define COMPILER "pgcc"
# define COMPILER_VERSION __PGIC__ __PGIC_MINOR __PGIC_PATCHLEVEL__
#endif
#ifndef COMPILER
# define COMPILER "unknown"
# define COMPILER_VERSION "unknown"
#endif

/* C Standard */
#ifdef __STDC_VERSION__
# define CSTANDARD __STDC_VERSION__
#endif
#ifndef CSTANDARD
# define CSTANDARD "unknown"
#endif

/* Platform */

#ifdef __APPLE__
# define PLATFORM "APPLE"
#elif __linux__
# define PLATFORM "LINUX"
#elif __unix__ // all unices, not all compilers
# define PLATFORM "UNIX"
#endif
#ifndef PLATFORM
# define PLATFORM "unknown"
#endif

#endif

'''


def main():

    version = git_version()

    header_text = version_header_template.format(version.full, version.short,
                                                 version.tag)

    write_version_header(header_text)


def write_version_header(header, filename=None):

    if not filename:
        mypath = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(mypath, os.pardir, 'vic', 'drivers', 'shared',
                                'include', 'version.h')

    with open(filename, 'w') as f:
        f.write(header)

    return


def git_version():
    pipe = None
    for git in ['git', 'git.cmd']:
        try:
            pipe = subprocess.Popen([git, 'describe', '--abbrev=4', '--dirty',
                                     '--always', '--tags'],
                                    stdout=subprocess.PIPE)
            (so, serr) = pipe.communicate()
            if pipe.returncode == 0:
                break
        except:
            pass
    if pipe is None or pipe.returncode != 0:
        #  no git, or not in git repo
        have_version = False
        warnings.warn("WARNING: Couldn't get git revision, using generic "
                      "version string")
    else:
        have_version = True
        rev = so.strip()
        if _py3:
            rev = rev.decode('ascii')

    if have_version:
        pipe = subprocess.Popen([git, 'log', '-1', '--format=%cd'],
                                stdout=subprocess.PIPE)
        (so, serr) = pipe.communicate()
        log = so.strip()
        if _py3:
            log = log.decode('ascii')

        pipe = subprocess.Popen([git, 'describe', '--abbrev=0'],
                                stdout=subprocess.PIPE)
        (so, serr) = pipe.communicate()
        tag = so.strip()
        if _py3:
            tag = log.decode('ascii')

        version.short = rev
        version.tag = tag
        version.full = '{0} {1}'.format(rev, log)

    return version


if __name__ == "__main__":
    main()
