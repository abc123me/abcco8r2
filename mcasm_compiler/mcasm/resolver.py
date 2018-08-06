# Resolves a program into it's symbols
def resolve(lines):
        print("Creating symbols")
        sym = []
        for l in lines:
                s = resolveLine(l)
                if(s == None):
                        continue
                sym.append(s)
                print("Resolved symbol: " + str(s))
        print("Done! Created " + str(len(sym)) + " symbols!")
        return sym
#Converts a line to its associated symbol
def resolveLine(line):
        line = cleanLine(line)
        if(len(line) <= 0):
                return None
        if(line.startswith(".")): #labels
                n = line[1:]
                print("Resolved label: " + n)
                return Symbol(n, "label")
        elif(line.startswith(";")): #compiler option
                n = line[1:]
                print("Resolved compiler option: " + n)
                return Symbol(n, "copt")
        elif(line.startswith("$")):
                parts = line[1:].split(" ")
                if(len(parts) != 2):
                        raise Exception("Error resolving compiler constant: " + line)
                n = parts[0]
                v = parts[1]
                print("Resolved compiler constant: %s (%s)" % (n, v))
                return Symbol(n, "const", False, v)
        else: #Assumed as an instruction
                parts = line.split(" ")
                n = parts[0]
                pars = []
                if(len(parts) > 1):
                        pars = parts[1:]
                n = n.strip()
                print("Resolved instruction: " + n)
                return Symbol(n, "instruction", True, pars)
        return None
