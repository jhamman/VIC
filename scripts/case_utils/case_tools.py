"""VIC setup command line interface"""
from __future__ import print_function
import os
import subprocess
from datetime import datetime, time


def create_makefile(template, makefile, casename, vicroot):
    '''Create ready to use makefile in case directory'''

    return


def make(makefile, logdir):
    '''wrapper function around the Unix make utility'''
    timestamp = get_timestamp()

    make_args = ['make', '-f', os.path.abspath(makefile)]

    proc = subprocess.Popen(make_args,
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    retvals = proc.communicate()

    stdout = retvals[0]
    stderr = retvals[1]
    returncode = proc.returncode

    # write stdout and stderr to file
    logfile = os.path.join(logdir, 'vic.bld.log.{0}.txt'.format(timestamp))
    logfile = os.path.abspath(logfile)
    with open(logfile, mode='wb') as f:
        f.write(stdout)
        f.write(stderr)

    if returncode:
        print('Error building VIC.')
        print('See log file for more information: {0}'.format(logfile))
        print(stderr)

        raise RuntimeError('Error Building VIC')

    return


def run(global_file, logdir):
    '''run vic simulation'''
    timestamp = get_timestamp()

    run_args = ['Build/bin/vic', '-g', os.path.abspath(global_file)]

    proc = subprocess.Popen(' '.join(run_args),
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    retvals = proc.communicate()

    stdout = retvals[0]
    stderr = retvals[1]
    returncode = proc.returncode

    # write stdout and stderr to file
    logfile = os.path.join(logdir, 'vic.run.log.{0}.txt'.format(timestamp))
    logfile = os.path.abspath(logfile)
    with open(logfile, mode='wb') as f:
        f.write(stdout)
        f.write(stderr)

    if returncode:
        print('Error runing VIC.')
        print('See log file for more information: {0}'.format(logfile))
        print(stderr)

    return returncode


def get_timestamp():
    "Get a timestamp format as YYYYMMDD.SSSSS"
    now = datetime.now()
    utcnow = datetime.utcnow()
    midnight_utc = datetime.combine(utcnow.date(), time(0))
    seconds = (utcnow - midnight_utc).total_seconds()
    timestr = now.strftime('%Y%m%d.{0:5d}'.format(int(seconds)))
    return timestr


def log_to_readme(fname, message):
    now = datetime.now()

    with open(fname, mode='a') as f:
        f.write('{time} : {message}'.format(time=now.isoformat(),
                                            message=message))
