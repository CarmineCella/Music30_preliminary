import collections
import numpy as np

NPREF = 2
NONWORD = "\n"
MAXGEN = 200

class Prefix:
    
    def __init__(self, n, string):
        self.__multiplier = 31
        self.p = collections.deque()
        
        for i in range(n):
            self.p.append(string)
        
    def __hash__(self):
        h = 0
        for i in range(len(self.p)):
            h = self.__multiplier * h + hash(self.p[i])
        return h
    
    def __eq__(self, other):
        for i in range(len(self.p)):
            if (self.p[i] != other.p[i]):
                return False
        return True
    
    def clone(self):
        copyP = self.p.copy()
        copy = Prefix(NPREF, NONWORD)
        copy.p = copyP
        return copy
    
class Chain:
    def __init__(self, NPREF = 2, NONWORD = "\n", MAXGEN = 200):
        # map<Prefix, vector<string>>
        self.statetab = {}
        self.NPREF = NPREF
        self.NONWORD = NONWORD
        self.MAXGEN = MAXGEN
        
        self.prefix = Prefix(self.NPREF, self.NONWORD)

    def add(self, string):
        suf =  self.statetab.get(self.prefix)
        if not suf:
            suf = []
            self.statetab[self.prefix.clone()] = suf
            
        suf.append(string)
        self.prefix.p.popleft()
        self.prefix.p.append(string)
        

    def build(self, inStream):
        for i in inStream:
            self.add(i)
        self.add(self.NONWORD)

    def generate(self, nwords):
        chain = []
        new = Prefix(self.NPREF, self.NONWORD)
        for i in range(0, nwords):
            s = self.statetab.get(new)
            
            if not s:
                return "No state"

            r = np.random.randint(0, 9999999999) % len(s)
            word = s[r]

            if word == self.NONWORD:
                break;
            chain.append(word)
            new.p.popleft()
            new.p.append(word)
        return chain