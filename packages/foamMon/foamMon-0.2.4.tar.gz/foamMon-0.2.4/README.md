# foamMon
![](https://badge.fury.io/py/owls.svg)

A simple tool for monitoring the progress of OpenFOAM simulations

![screenshot](https://github.com/greole/foamMon/blob/master/.assets/screen.png)

# Installation

foamMon can be installed from the Pypi repositories

    pip3 install foamMon

or directly from this repo

    python3 setup.py install --user

or

    pip install foamMon

## Ubuntu

If installing under ubuntu with user privileges make sure that
'$HOME/.local/bin' is added to your '$PATH'. If necessary
add

    export PATH=$PATH:$HOME/.local/bin

to your ~/.bashrc file

# Usage

To monitor the progress of simulations simply run 'foamMon' in a parent directory.

# Logfiles

The log files need to have *log* in the filename.

