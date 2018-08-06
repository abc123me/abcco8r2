class Symbol:
        def __init__(self, name, stype, hasAddress = False, params = []):
                self.name = name
                self.type = stype
                self.hasAddress = hasAddress
                self.params = params
        def __str__(self):
                pstr = ""
                if(len(self.params) > 0):
                        pstr = " with params " + str(self.params)
                cstr = " (ignored)"
                if(self.hasAddress):
                        cstr = " (addressable)"
                return str(self.name) + " of type \"" + str(self.type) + "\"" + pstr + cstr
class Instruction:
        def __init__(self, name, addr, vals):
                self.name = name
                self.addr = addr
                self.vals = vals
