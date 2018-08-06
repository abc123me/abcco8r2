def getArg(args, triggers, default, hasArg=True, exists=True, validOptions=None, invalid=None):
	i = 0
	for i in range(0, len(args)):
		arg = args[i].strip()
		if arg in triggers:
			j = i + 1
			if hasArg:
				if j >= len(args):
					raise Exception("No argument provided for %s" % (str(args[i])))
				opt = args[j]
				if(validOptions != None):
					if(opt in validOptions):
						return opt
					else:
						return invalid
				else:
					return opt
			else:
				return exists
	return default
def intb(s):
	s = str(s)
	if(s.startswith("0x")):
		return int(s[2:], 16)
	if(s.startswith("0b")):
		return int(s[2:], 2)
	if(s.startswith("0d")):
		return int(s[2:], 10)
	return int(s)
def parseKeyVal(text, oarr=True, retab=True):
	if(retab):
		text.replace("\t", " ")
	if(":" not in text):
		raise ValueError("Not a key value pair (key: value(s))!")
	parts = text.split(":")
	if(len(parts) != 2):
		raise ValueError("Not a key value pair (key: value(s))!")
	key = parts[0].strip()
	if(oarr):
		val = []
		for v in parts[1].strip().split(" "):
			val.append(v.strip())
		return (key, val)
	else:
		if(len(parts) > 2):
			raise ValueError("Not a key value pair (key: value)!")
		return (key, parts[1].strip())
def parseKeyValFile(fname, clean=True, oarr=True, retab=True):
	kvs = {}
	with open(fname, "r") as f:
		for l in f.readlines():
			if(clean):
				l = cleanLine(l)
			if(len(l) <= 0):
				continue;
			kv = parseKeyVal(l, oarr, retab)
			kvs[kv[0]] = kv[1]
	return kvs
def cleanLine(l, retab=True):
	if("#" in l):
		l = l[:l.index("#")]
	if(retab):
		l = l.replace("\t", " ")
	l = l.strip()
	return l
