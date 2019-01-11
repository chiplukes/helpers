'''
Sets up right click explorer context menu for Neovim in Windows 10

Prerequisites:
1) Neovim installed somewhere (see NEOVIM_INSTALL_LOCATION below)

Steps:
1) download desired release from https://github.com/neovim/neovim/releases
2) I extract files into c:/tools/Neovim
3) run this script!

'''

import os
import winreg as reg
import ctypes, sys
from pathlib import Path


NEOVIM_INSTALL_LOCATION = r'C:\tools\Neovim'



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def deleteSubkey(key0, key1, key2=""):
    if key2=="":
        currentkey = key1
    else:
        currentkey = key1+ "\\" +key2

    open_key = reg.OpenKey(key0, currentkey ,0,reg.KEY_ALL_ACCESS)
    infokey = reg.QueryInfoKey(open_key)
    for x in range(0, infokey[0]):
        #NOTE:: This code is to delete the key and all subkeys.
        #  If you just want to walk through them, then
        #  you should pass x to EnumKey. subkey = reg.EnumKey(open_key, x)
        #  Deleting the subkey will change the SubKey count used by EnumKey.
        #  We must always pass 0 to EnumKey so we
        #  always get back the new first SubKey.
        subkey = reg.EnumKey(open_key, 0)
        try:
            reg.DeleteKey(open_key, subkey)
            print("Removed %s\\%s " % ( currentkey, subkey))
        except:
            deleteSubkey( key0, currentkey, subkey )
            # no extra delete here since each call
            #to deleteSubkey will try to delete itself when its empty.

    reg.DeleteKey(open_key,"")
    open_key.Close()
    print("Removed %s" % (currentkey))
    return


if is_admin() == False:
    print("not admin")
    # Re-run the program with admin rights
    cf = Path.cwd()/__file__
    print(cf)
    print("runas", r'cmd.exe', r'/C {} {} & pause'.format(sys.executable, cf))
    print(ctypes.windll.shell32.ShellExecuteW(None, "runas", r'cmd.exe', r'/C {} {} & pause'.format(sys.executable, cf), None, 1))
else:
    # Code of your program here
    print("admin")

    # names of all overlay icons that shall be boosted:
    # right click list [['menu_name', 'command_path', 'icon_path']]
    rcl = []
    rcl.append([' Edit with NeoVim', r'"{}\bin\nvim-qt.exe" "%1"'.format(NEOVIM_INSTALL_LOCATION), r'"{}\bin\nvim-qt.exe"'.format(NEOVIM_INSTALL_LOCATION)])

    with reg.OpenKey(reg.HKEY_CLASSES_ROOT, r'*\shell') as base:
        for r in rcl:

            # search through existing keys
            i = 0
            while True:
                try:
                    name = reg.EnumKey(base, i)
                except WindowsError:
                    break

                # check if already present
                core = name.strip()
                #print(core, name)

                if r[0] == name:
                    print('Delete', repr(core))
                    deleteSubkey(base, name)
                    #reg.DeleteKey(base, name)
                    break
                i += 1

            # add key
            print("Adding Key: {}", r[0])
            newkey = reg.CreateKey(base, r[0])
            # command subkey
            reg.SetValue(newkey, 'command', reg.REG_SZ, r[1])
            # Icon value
            reg.SetValueEx(newkey, 'Icon', 0, reg.REG_SZ, r[2])
