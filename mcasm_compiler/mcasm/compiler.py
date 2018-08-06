#!/usr/bin/python3

import ccompiler as compiler
from cutils import *

def getInstructionMap(loc="imap"):
	return parseKeyValFile(loc)
def getRegisterMap(loc="rmap"):
	return parseKeyValFile(loc, oarr=False)
def parseArgs(args):
	cfg = {"exit": False, "exit_code": 0}
	help = getArg(args, ["-h", "-H", "-?", "--help"], False, False)
	if(help):
		printHelp(args[0])
		cfg["exit"] = True
		return cfg
	cfg["imap"] = getArg(args, ["-I", "--imap"], "imap")
	cfg["rmap"] = getArg(args, ["-R", "--rmap"], "rmap")
	cfg["input_file"] = getArg(args, ["-i"], args[len(args) - 1])
	cfg["output_file"] = getArg(args, ["-o"], None)
	asmDefault = "hex"
	casm = getArg(args, ["-a", "--assembler"], asmDefault, validOptions=["logisim", "hex"], invalid=None)
	if(casm == None):
		print("Invalid assembler, defaulting to %s!" % (asmDefault))
		casm = asmDefault
	cfg["assembler"] = casm
	return cfg
def printHelp(cmd):
	print("ABCco8r2 compiler help:")
	print("Usage: %s <arguments> <input_file>" % (cmd))
	print("Arguments:")
	print("\t-i <input_file>: Declares the input file")
	print("\t-o <output_file>: Declares the output file (default print to stdout)")
	print("\t-R, --rmap <registry_map>: Declares a custom register map (default \"rmap\")")
	print("\t-I, --imap <instruction_map>: Declares a custom instruction map (default \"imap\")")
	print("\t-h, -H, -?, --help: Displays this help")
	print("\t-a, --assembler <assembler_name>: Chooses the assembler (default \"hex\")")
	print("Assemblers (default hex):")
	print("\tlogisim: Logisim image")
	print("\thex: Hex values for every instruction seperated by a space")
def main(args):
	if(len(args) < 2):
		printHelp(args[0])
		exit(0)
	cfg = parseArgs(args)
	if(cfg["exit"]):
		exit(cfg["exit_code"])
	print("Loading instruction map: " + cfg["imap"], end="")
	imap = getInstructionMap(cfg["imap"])
	print(" [OK]\nLoading register map: " + cfg["rmap"], end="")
	rmap = getRegisterMap(cfg["rmap"])
	print(" [OK]")

	ifile = open(cfg["input_file"], "r")
	symbols = compiler.resolve(ifile.readlines())
	ifile.close()
	compilationUnit = compiler.compile(symbols)
	linkedAssembly = compiler.link(compilationUnit, imap, rmap)

	res = None
	asmt = cfg["assembler"]
	if(asmt == "hex"):
		print("Assembling as a hex string")
		res = compiler.assembleString(linkedAssembly)
	elif(asmt == "logisim"):
		print("Assembling as a logisim binary image")
		res = compiler.assembleLogisim(linkedAssembly)
	print("Assembled successfully!")
	of = cfg["output_file"]
	if(of == None):
		print(res)
	else:
		print("Writing to %s" % of)
		out = open(of, "w")
		out.write(res)
		out.close()

if(__name__ == "__main__"):
	from sys import argv
	main(argv)
