# abcco8r2
8 bit CPU in longisim (revision 2)

# Compiling
The `compile` script used in this video will NOT work on windows, its a linux shell script.

However, the compiler script was made in python so it should work perfectly fine on windows
The command to launch the compiler on windows should be, assuming you have python in your path:
`python3 compiler.py -i INPUT_FILENAME.mcasm -a logisim -o OUTPUT_FILENAME.mcasm`
The `compile` script is just a shortcut for that long command
