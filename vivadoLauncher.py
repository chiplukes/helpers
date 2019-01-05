#!/usr/bin/env python3
"""
launcher for Vivado files.

extracts the vivado version from the following:
 - in *.xpr:  "<!-- Product Version: Vivado v2018.1"

"""
import os
import sys
import platform
from subprocess import Popen, PIPE
import argparse
from pathlib import Path

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help = 'full path to a *.xpr file')
    args = parser.parse_args()
    xpr_file = Path(args.file)

    if not xpr_file.exists():
        print('File not found : {} '.format(xpr_file))
        input("Here")
        exit(1)
    else:
        with open(xpr_file, 'r') as f:
            ifile = f.readlines()
        srch = "<!-- Product Version: Vivado v"
        for r in ifile:
            if srch in r:
                s = r.split(srch)
                vivado_version = s[1]

    vivado_version = vivado_version.split(' ')[0]
    s = vivado_version.split('.')
    ver_maj, ver_min = s[0], s[1]

    # set system/version dependent "start_new_session" analogs
    kwargs = {}
    if platform.system() == 'Windows':
        # from msdn [1]
        CREATE_NEW_PROCESS_GROUP = 0x00000200  # note: could get from subproc
        DETACHED_PROCESS = 0x00000008          # 0x8 | 0x200 == 0x208
        kwargs.update(creationflags=DETACHED_PROCESS |
                      CREATE_NEW_PROCESS_GROUP)

        vvgl = Path('C:/Xilinx/Vivado/{}.{}/bin/unwrapped/win64.o/vvgl.exe'.format(ver_maj,ver_min))
        if not vvgl.exists():
            print('File not found : {} '.format(vvgl))
            exit(1)

        vbat = Path('C:/Xilinx/Vivado/{}.{}/bin/vivado.bat'.format(ver_maj,ver_min))
        if not vbat.exists():
            print('File not found : {} '.format(launch))
            exit(1)

        launch_cmd = [str(vvgl), str(vbat), str(xpr_file)]

    elif sys.version_info < (3, 2):  # assume posix
        kwargs.update(preexec_fn=os.setsid)
        linux_vivado_exe = Path(f'/opt/Xilinx/Vivado/{ver_maj}.{ver_min}/bin/vivado')
        launch_cmd = [str(linux_vivado_exe), str(xpr_file)]
    else:  # Python 3.2+ and Unix
        kwargs.update(start_new_session=True)
        linux_vivado_exe = Path(f'/opt/Xilinx/Vivado/{ver_maj}.{ver_min}/bin/vivado')
        launch_cmd = [str(linux_vivado_exe), str(xpr_file)]

    p = Popen(launch_cmd, stdin=PIPE, stdout=PIPE,
                stderr=PIPE, **kwargs)
