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
        
    def eval(self, writer):
        for inst in self.instList:
            inst.eval(writer)

            

        

class ArithmOp:
    def __init__(self, operator, leftarg, rightarg):
        self.leftarg = leftarg
        self.rightarg = rightarg
        self.operator = operator
        
    def eval(self, writer):
        self.leftarg.eval(writer)
        self.rightarg.eval(writer)
        self.id = IdGenerator.getNextId()
        writer.append(self.id + " = " + self.leftarg.id +" "+self.operator+" "+self.rightarg.id)
        
class AssignOp:
    def __init__(self, leftarg, rightarg):
        self.leftarg = leftarg
        self.rightarg = rightarg
        
    def eval(self, writer):
        self.leftarg.eval(writer)
        self.rightarg.eval(writer)
        writer.append(self.leftarg.id + " = " + self.rightarg.id)
        self.id = self.leftarg.id

class CompOp:
    def __init__(self, operator, leftarg, rightarg):
        self.leftarg = leftarg
        self.rightarg = rightarg
        self.operator = operator
    
    def eval(self, writer):
        self.leftarg.eval(writer)
        self.rightarg.eval(writer)
        
        self.leftid = self.leftarg.id
        self.rightid = self.rightarg.id
    
class While:
    def __init__(self, condition, body):
        self.body = body;
        self.condition = condition;
        
    def eval(self, writer):
        conditionStartLine = writer.getLen()
        self.condition.eval(writer)
        conditionCheckLine = writer.reserveLine()
        self.body.eval(writer)
        writer.append("if== 1 1 "+str(conditionStartLine))
        afterWhileLine = writer.getLen()
        writer.putLine(conditionCheckLine, Utils.getIfCond(self.condition, afterWhileLine))

class If(object):
    def __init__(self, condition, ifbody):
        self.condition = condition
        self.ifbody = ifbody
        
    def eval(self, writer):
        self.condition.eval(writer)
        lineno = writer.reserveLine()
        self.ifbody.eval(writer)
        jumpLine = writer.getLen()
        writer.putLine(lineno, Utils.getIfCond(self.condition, jumpLine))
        
class IfElse(If):
    def __init__(self, condition, ifbody, elsebody):
        self.condition = condition
        self.ifbody = ifbody
        self.elsebody = elsebody
        
    def eval(self, writer):
        self.condition.eval(writer)
        ifCondLine = writer.reserveLine()
        self.ifbody.eval(writer)
        afterIfStmtLine = writer.reserveLine()
        elseStartLine = writer.getLen()
        self.elsebody.eval(writer)
        afterElseLine = writer.getLen()
        writer.putLine(ifCondLine, Utils.getIfCond(self.condition, elseStartLine))
        writer.putLine(afterIfStmtLine, "if== 1 1 "+str(afterElseLine))
        
        
class Constant:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.id = value
        
    def eval(self, writer):
        pass
    
class Variable:
    def __init__(self, name):
        self.name = name
        self.id = name

    def eval(self, writer):
        pass

class Declarations:
    def __init__(self):
        self.dic = dict()
    def append(self, name, type):
        if name in self.dic:
            raise NameError("Duplicated Variable!")
        self.dic[name] = type
    def sum(self, other):
        for (name, type) in other.dic.items():
            self.append(name, type)