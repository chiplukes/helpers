#!/usr/bin/env python
"""
Sets up Neovim in windows

Prerequisites:
1) git needs to be installed
2) PLUG_MANAGER set to something (Ie. vim-plug, etc.)
3) INIT_VIM_LOCATION points to init.vim at some git repo
4) Might need to turn on developer options in Windows 10 so that symbolic links work!

Steps:
1) download desired release from https://github.com/neovim/neovim/releases
2) I extract files into c:/tools/Neovim
3) run this script!
"""
import subprocess
import argparse
import os
from pathlib import Path
import ctypes

PLUG_MANAGER = r'https://github.com/junegunn/vim-plug.git'
INIT_VIM_LOCATION = r'https://github.com/chiplukes/init.vim.git'

def cmdex(cmd):
    '''
    calls cmd /c cmd at the command line
    '''
    if '~' in cmd:
        cmd = cmd.replace('~', r'{}{}'.format(os.environ['HOMEDRIVE'],os.environ['HOMEPATH']))

    print('Running command > {}'.format(cmd))
    result = subprocess.run(['cmd', '/c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode:
        print("Failed: ",  result.stderr)

def cmdex_admin(cmd):
    '''
    calls a admin command line
    '''
    if '~' in cmd:
        cmd = cmd.replace('~', r'{}{}'.format(os.environ['HOMEDRIVE'],os.environ['HOMEPATH']))

    print('Running admin command (new shell) > {}'.format(cmd))
    ctypes.windll.shell32.ShellExecuteW(None, "runas", r'cmd.exe', r'/C "{}" & pause'.format(cmd), None, 1)


def rm(f):
    '''
    removes file, folder etc
    '''
    if '~' in f:
        f = f.replace('~', r'{}{}'.format(os.environ['HOMEDRIVE'],os.environ['HOMEPATH']))

    f_pth = Path(f)
    if f_pth.is_file() or f_pth.is_symlink():
        cmdex(r'del {}'.format(f_pth))
    elif f_pth.is_dir:
        cmdex(r'rmdir {} /s /Q'.format(f_pth))

if __name__ == '__main__':

    # Code of your program here
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store_true', help = 'uninstall Neovim')
    parser.add_argument('-i', action='store_true', help = 'install Neovim')
    args = parser.parse_args()

    if args.i:
        cmdex(r'md ~\AppData\Local\nvim\autoload')
        cmdex(r'git clone {} ~\AppData\Local\nvim\autoload'.format(PLUG_MANAGER))
        cmdex(r'md ~\AppData\Local\nvim\.config')
        cmdex(r'git clone {} ~\AppData\Local\nvim\.config'.format(INIT_VIM_LOCATION))
        #cmdex(r'mklink ~\AppData\Local\nvim\init.vim ~\AppData\Local\nvim\.config\init.vim')
        cmdex_admin(r'mklink ~\AppData\Local\nvim\init.vim ~\AppData\Local\nvim\.config\init.vim')
        cmdex('setx XDG_CONFIG_HOME ~\AppData\Local')

    elif args.u:
        rm(r'~\AppData\Local\nvim\autoload')
        rm(r'~\AppData\Local\nvim\.config')
        rm(r'~\AppData\Local\nvim\init.vim')
        cmdex('setx XDG_CONFIG_HOME ""')

    else:
        print("Not doing anything, specify -i or -u options")