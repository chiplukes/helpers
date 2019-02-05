#!/usr/bin/env python
"""
launcher for Vivado tcl scripts.

extracts the vivado version from the following:
 - in *.tcl:  "set scripts_vivado_version 2018.1"

"""
import subprocess
import argparse
from pathlib import Path
import platform
import sys
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help = 'full path to a *.tcl file')
    args = parser.parse_args()
    p = Path(args.file)

    bd_file = p.parent/'mk_bd.tcl'
    ip_file = p.parent/'mk_ip.tcl'
    if ip_file.exists():
        # check if in IP folder of a project
        pnew = p.parent
        pnew = pnew.parent
        bd_file = p.parent/'mk_bd.tcl'

    vivado_version = None
    if not bd_file.exists():
        vivado_version = input('Enter Vivado shell version 20xx.x: ')
    else:
        with open(bd_file, 'r') as f:
            ifile = f.readlines()
        srch = "set scripts_vivado_version "
        for r in ifile:
            if srch in r:
                s = r.split(srch)
                vivado_version = s[1].rstrip()
        if vivado_version is None:
            vivado_version = input('Enter Vivado shell version 20xx.x: ')

    s = vivado_version.split('.')
    ver_maj, ver_min = s[0], s[1]

    kwargs = {}
    if platform.system() == 'Windows':

        launch = Path('C:/Xilinx/Vivado/{}.{}/bin/vivado.bat'.format(ver_maj,ver_min))
        launch_cmd = [str(launch)]
        if not launch.exists():
            print('File not found : {} '.format(launch))
            exit(1)
        p = subprocess.call([str(launch), '-mode', 'tcl'])

    elif sys.version_info < (3, 2):  # assume posix
        kwargs.update(preexec_fn=os.setsid)
        linux_vivado_exe = Path(f'/opt/Xilinx/Vivado/{ver_maj}.{ver_min}/bin/vivado')
        launch = f'xterm -e ' + f'{linux_vivado_exe.resolve()} -mode tcl'
        if not linux_vivado_exe.exists():
            print('File not found : {} '.format(launch))
            exit(1)
        p = subprocess.Popen(f'{launch}',
                            cwd=f'{(p.parent).resolve()}',
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, **kwargs)

    else:  # Python 3.2+ and Unix
        kwargs.update(start_new_session=True)
        linux_vivado_exe = Path(f'/opt/Xilinx/Vivado/{ver_maj}.{ver_min}/bin/vivado')
        launch = f'xterm -e ' + f'{linux_vivado_exe.resolve()} -mode tcl'
        if not linux_vivado_exe.exists():
            print('File not found : {} '.format(launch))
            exit(1)
        p = subprocess.Popen(f'{launch}',
                            cwd=f'{(p.parent).resolve()}',
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, **kwargs)


