#!/usr/bin/python3
from cutils import *
from cclasses import *
# Resolves a program into it's symbols
def resolve(lines, verbose=False):
	print("Creating symbols")
	sym = []
	line = 0
	for l in lines:
		line = line + 1
		s = resolveLine(l, verbose)
		if(s == None):
			continue
		sym.append(s)
	print("Done! Created " + str(len(sym)) + " symbols!")
	return sym
#Converts a line to its associated symbol
def resolveLine(line, verbose=False):
	line = cleanLine(line)
	if(len(line) <= 0):
		return None
	if(line.startswith(".")): #labels
		n = line[1:]
		if(verbose):
			print("Resolved label: " + n)
		return Symbol(n, "label")
	elif(line.startswith(";")): #compiler option
		n = line[1:]
		if(verbose):
			print("Resolved compiler option: " + n)
		return Symbol(n, "copt")
	elif(line.startswith("$")):
		parts = line[1:].split(" ")
		if(len(parts) != 2):
			raise Exception("Error resolving compiler constant: " + line)
		n = parts[0]
		v = parts[1]
		if(verbose):
			print("Resolved compiler constant: %s (%s)" % (n, v))
		return Symbol(n, "const", False, v)
	else: #Assumed as an instruction
		parts = line.split(" ")
		n = parts[0]
		pars = []
		if(len(parts) > 1):
			pars = parts[1:]
		n = n.strip()
		if(verbose):
			print("Resolved instruction: " + n)
		return Symbol(n, "instruction", True, pars)
	return None
#Compiles the symbols into a set of instructions and assigns the addresses to the labels
def compile(symbols, verbose=False):
	print("Compiling!")
	labels = {}
	consts = {}
	addr = 0
	inst = []
	for i in range(0, len(symbols)):
		s = symbols[i]
		n = str(s.name)
		if(s.type == "instruction"):
			inst.append(Instruction(n, addr, s.params))
			if(verbose):
				print("Assigning instruction %s to address 0x%x with params %s" % (n, addr, str(s.params)))
		elif(s.type == "label"):
			labels[n] = addr
			print("Assigning label %s to address 0x%x" % (n, addr))
		elif(s.type == "copt"):
			print("[WARNING] Copts not yet implemented!")
		elif(s.type == "const"):
			val = intb(s.params)
			print("Constant %s = 0x%x" % (n, val))
			consts[n] = val
		else:
			raise Exception("Unknown symbol at " + hex(addr) + ": " + str(s))
		if(s.hasAddress):
			addr = addr + 1
	print("Done!")
	return (labels, inst, consts)
# Creates a linker array used by link() to make a binary
# Takes: Pre resolved symbols (string list)
#       Instruction map (dictionary)
#               -Key: Instruction name
#               -Value: List of ORDERED data
#                       -Instruction value
#                       -Instruction size
#                       -Parameter amount
#                       -Parameter 0 type
#                       -Parameter 1 type
#                       -Parameter n type
#       Register map (dictionary)
#               -Key: Register name
#               -Value: Register address
# Links the names to thier actual values and returns an assembly unit
def link(cunit, imap, rmap, verbose=False):
	labels = cunit[0]
	inst = cunit[1]
	consts = cunit[2]
	asm = []
	print("Linking!")
	for i in inst:
		n = i.name
		if(not n in imap):
			raise Exception("Instruction %s not found in instruction map!" % (n)) 
		types = imap[n]
		pp = len(i.vals)
		rp = intb(types[2])
		lt = intb(types[1])
		if(lt < 1 or rp < 0 or lt <= rp):
			raise Exception("Invalid instruction size (%i) or parameter amount (%i)" % (lt, rp))
		if(rp != pp):
			raise Exception("Not enough parameters for instruction: %s (needs: %i given: %i)" % (n, lt, pp))   
		val = intb(types[0])
		pvals = [0] * (lt - 1)
		for j in range(0, pp):
			v = str(i.vals[j])
			pvals[j] = getValue(v, types[3 + j], rmap, labels, consts)
		tval = val
		for i in range(0, len(pvals)):
			tval = tval << 8
			tval = tval + pvals[i]
		asm.append(tval)
		if(verbose):
			print("Parsed instruction: " + hex(tval))
	print("Done!")
	return asm
def getValue(v, t, rmap, labels, consts):
	dc = decomp(v, "$", consts, "Constant")
	if(dc != None):
		return dc
	dc = decomp(v, ".", labels, "Label")
	if(dc != None):
		return dc
	dc = decomp(v, "%", rmap, "Register")
	if(dc != None):
		return dc
	if(t == "zero"):
		return 0
	elif(t == "label" and v in labels):
		return labels[v]
	elif(t == "register" and v in rmap):
		return intb(rmap[v])
	else:
		return intb(v)
def decomp(sr, cmpstr, dic, typ):
	s = sr
	if(sr.startswith(cmpstr)):
		val = sr[1:]
		if(val in dic):
			dv = intb(dic[val])
			print("%s found, filling it with its value (%s)" % (typ, hex(dv)))
			return dv
		else:
			raise Exception("%s %s does not exist!" % (typ, val))
	return None
#Assembles the program as a string
def assembleString(asm, sep=" ", base=16):
	out = ""
	for ins in asm:
		h = hex(ins)[2:]
		out = out + h + sep
	e = len(out) - len(sep)
	if(e < 0):
		e = 0
	return out[:e]
#Assembles the program as a logism image, returns the file data
def assembleLogisim(asm, header="v2.0 raw\n", ipl=16, nl="\n"):
	b = 0
	out = header
	for ins in asm:
		w = hex(ins)[2:]
		b = b + 1
		if(b % ipl == 0):
			w = w + nl
		else:
			w = w + " "
		out = out + w
	return out
