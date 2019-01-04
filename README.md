# helpers
Various helper scripts (Ie. launch correct vivado version for a xpr file when multiple Vivado installs, etc.)

vivadoLauncher.py - parses the *.xpr file to determine which Vivado version should open the project.  (This was born of frustration that the most recently installed vivado will always open when you double click on a *.xpr file)

vivadoShell.py - opens a Vivado shell, looks for version in my mk_bd.tcl file, otherwise lets you type the version you want.

setupRegistryVivado.py - running this in windows 10 will add Right click context menu items for vivadoLauncher and vivadoShell
