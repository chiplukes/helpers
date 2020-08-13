'''
https://cito.github.io/blog/overlay-icon-battle/
'''

'''
Computer\HKEY_CLASSES_ROOT\*\shell

ConEmu Vivado (folder)
  string named Icon with data= 'C:\tools\cmdermini\vendor\conemu-maximus5\ConEmu64.exe,0'
  key named commmand
     "C:\tools\cmdermini\vendor\conemu-maximus5\ConEmu64.exe" -here -run {Vivado2016_3} -cur_console:n

'''

import os
import winreg as reg
import ctypes, sys
import pathlib

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

    print()

    # Re-run the program with admin rights
    cf = pathlib.Path.cwd()/__file__
    print(cf)
    print("runas", r'cmd.exe', r'/C {} {} & pause'.format(sys.executable, cf))
    print(ctypes.windll.shell32.ShellExecuteW(None, "runas", r'cmd.exe', r'/C {} {} & pause'.format(sys.executable, cf), None, 1))
else:
    # Code of your program here
    print("admin")
    cwd = pathlib.Path(__file__).parent.absolute()
    print(cwd)

    # names of all overlay icons that shall be boosted:
    # right click list [['menu_name', 'command_path', 'icon_path']]
    rcl = []
    #rcl.append(['Vivado Launch', r'C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe  -Command python c:\Projects\helpers\VivadoLauncher.py --file "%1"', r'C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe'])
    rcl.append(['Vivado Launch', f'powershell.exe  -Command python "{str(cwd / "VivadoLauncher.py")}" --file "%1"', f'powershell.exe'])
    #rcl.append(['Vivado Shell', r'C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command python "C:\Projects\helpers\vivadoShell.py" --file "%1"', r'C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe'])
    rcl.append(['Vivado Shell', f'powershell.exe -NoExit -Command python "{str(cwd / "vivadoShell.py")}" --file "%1"', f'powershell.exe'])

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
