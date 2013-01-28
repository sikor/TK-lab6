class Utils:
    opposite = {">": "<=", 
    "<=" : ">", 
    "<" : ">=", 
    ">=": "<", 
    "==": "!=",
    "!=": "==",
    }

    @staticmethod
    def getOpositeOp(op):
        return Utils.opposite[op]
        
    @staticmethod
    def getIfCond(condition, jumpLine):
        operator = Utils.getOpositeOp(condition.operator) # if condition is not fulfilled jump to the end of if statement
        return "if"+operator+" "+condition.leftid+" "+condition.rightid+" "+str(jumpLine)
        
        
class IdGenerator:
    count = 0

    @staticmethod
    def getNextId():
        IdGenerator.count = IdGenerator.count + 1
        return "%mem"+str(IdGenerator.count)
        
class LineWriter:

    def __init__(self):
        self.lines = []
        
    def append(self, line):
        self.lines.append(line)
        
    def getLen(self):
        return len(self.lines)
        
    def reserveLine(self):
        self.lines.append("")
        return len(self.lines)-1
    
    def putLine(self, number, line):
        self.lines[number] = line
        
    def getLines(self):
        return self.lines

class InstList:
    def __init__(self):
        self.instList = []
        
    def append(self, inst):
        self.instList.append(inst)
        
    

            

        

class ArithmOp:
    def __init__(self, operator, leftarg, rightarg, lineno):
        self.leftarg = leftarg
        self.rightarg = rightarg
        self.operator = operator
        self.lineno = lineno
        
    
        
class AssignOp:
    def __init__(self, leftarg, rightarg, lineno):
        self.leftarg = leftarg
        self.rightarg = rightarg 
        self.lineno = lineno
        
    

class CompOp:
    def __init__(self, operator, leftarg, rightarg, lineno):
        self.leftarg = leftarg
        self.rightarg = rightarg
        self.operator = operator
        self.lineno = lineno
    
    
    
class While:
    def __init__(self, condition, body, lineno):
        self.body = body
        self.condition = condition 
        self.lineno = lineno
        
    

class If(object):
    def __init__(self, condition, ifbody, lineno):
        self.condition = condition
        self.ifbody = ifbody
        self.lineno = lineno
        
    
        
class IfElse(If):
    def __init__(self, condition, ifbody, elsebody, lineno):
        self.condition = condition
        self.ifbody = ifbody
        self.elsebody = elsebody    
        self.lineno = lineno
        
    
        
        
class Constant:
    def __init__(self, value, type, lineno):
        self.value = value
        self.type = type
        self.id = value
        self.lineno = lineno
        
    
    
class Variable:
    def __init__(self, name, lineno):
        self.name = name
        self.id = name
        self.lineno = lineno

    

class Declarations:
    def __init__(self):
        self.dic = dict()
    def append(self, name, type, lineno):
        if name in self.dic:
            #raise NameError("Duplicated Variable!")
            print("before " + str(lineno) + ": Duplicated variable: " + name)
            exit()
        self.dic[name] = type
    def sum(self, other, lineno):
        for (name, type) in other.dic.items():
            self.append(name, type, lineno)
            
            