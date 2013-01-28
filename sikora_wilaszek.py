#!/usr/bin/python

import sys;
import ply.lex as lex;
import ply.yacc as yacc;
from AST import *;
from pprint import pprint;
from typesOf import Types;


INT_TYPE = "int"
FLOAT_TYPE = "float"
STRING_TYPE = "str"

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

'''
                                                                                    
,--------.                       ,-----.,--.                  ,--.                  
'--.  .--',--. ,--.,---.  ,---. '  .--./|  ,---.  ,---.  ,---.|  |,-. ,---. ,--.--. 
   |  |    \  '  /| .-. || .-. :|  |    |  .-.  || .-. :| .--'|     /| .-. :|  .--' 
   |  |     \   ' | '-' '\   --.'  '--'\|  | |  |\   --.\ `--.|  \  \\   --.|  |    
   `--'   .-'  /  |  |-'  `----' `-----'`--' `--' `----' `---'`--'`--'`----'`--'    
          `---'   `--'                                                              
                                                                          '''

class TypeChecker:

    @addToClass(InstList)
    def check(self, types, declarations):
        flag = True
        for inst in self.instList:
            if(inst.check(types, declarations) == types.error()):
                flag = False
                
        if(flag):
            return 'int'
        else:
            return types.error()
         
         
    @addToClass(Constant)
    def check(self, types, declarations):
        return self.type
    
    @addToClass(Variable)
    def check(self, types, declarations):
        if(self.name not in declarations.dic.keys()):
            print(str(self.lineno) + ": Undeclared variable: " + self.name)
            return types.error()
            
        return declarations.dic[self.name]
    
    
    @addToClass(ArithmOp)
    def check(self, types, declarations):
        leftargType = self.leftarg.check(types, declarations)
        rightargType = self.rightarg.check(types, declarations)
        
        if(leftargType == types.error() or rightargType == types.error()):
            return types.error()
            
        opType = types.checkType(self.operator, leftargType, rightargType)
        #print("DEBUG: " + leftargType + " " + rightargType + " " + self.operator + " " + opType)
        if(opType == types.error()):
            print (str(self.lineno) + ": Type error in arithmetic operation. Forbidden arguments for operator: " + self.operator)
        return opType
    
    @addToClass(AssignOp)
    def check(self, types, declarations):
        leftargType = self.leftarg.check(types, declarations)
        rightargType = self.rightarg.check(types, declarations)
        
        if(leftargType == types.error() or rightargType == types.error()):
            return types.error()
        
        if(leftargType != rightargType):
            #print("DEBUG:  " + self.leftarg.name)
            print (str(self.rightarg.lineno) + ": Type error in assignment operation.")
            return types.error()
        else:
            return leftargType
        
    @addToClass(CompOp)
    def check(self, types, declarations):
        leftargType = self.leftarg.check(types, declarations)
        rightargType = self.rightarg.check(types, declarations)
        
        if(leftargType == types.error() or rightargType == types.error()):
            return types.error()
            
        opType = types.checkType(self.operator, leftargType, rightargType)
        if(opType == types.error()):
            print (str(self.lineno) + ": Type error in comparing operation.")
        return opType
    
    @addToClass(While)
    def check(self, types, declarations):
        if(self.condition.check(types, declarations) != 'int'):
            print(str(self.condition.lineno) + ": Type error in while loop condition.")
            return types.error()
        
        return self.body.check(types, declarations)
        
    @addToClass(If)
    def check(self, types, declarations):
        if(self.condition.check(types, declarations) != 'int'):
            print(str(self.condition.lineno) + ": Type error in If condition.")
            return types.error()
        
        return self.ifbody.check(types, declarations)
        
    @addToClass(IfElse)
    def check(self, types, declarations):
        if(self.condition.check(types, declarations) != 'int'):
            print(str(self.condition.lineno) + ": Type error in If-Else condition.")
            return types.error()
        
        if( self.ifbody.check(types, declarations) == types.error() ):
            return types.error()
            
        return self.elsebody.check(types, declarations)

    

'''
                                                                                                   
 ,-----.          ,--.        ,----.                                          ,--.                 
'  .--./ ,---.  ,-|  | ,---. '  .-./    ,---. ,--,--,  ,---. ,--.--. ,--,--.,-'  '-. ,---. ,--.--. 
|  |    | .-. |' .-. || .-. :|  | .---.| .-. :|      \| .-. :|  .--'' ,-.  |'-.  .-'| .-. ||  .--' 
'  '--'\' '-' '\ `-' |\   --.'  '--'  |\   --.|  ||  |\   --.|  |   \ '-'  |  |  |  ' '-' '|  |    
 `-----' `---'  `---'  `----' `------'  `----'`--''--' `----'`--'    `--`--'  `--'   `---' `--'    
                                                                                                   
'''

class CodeGenerator:
    
    @addToClass(InstList)
    def eval(self, writer):
        for inst in self.instList:
            inst.eval(writer)
            
    
    @addToClass(ArithmOp)
    def eval(self, writer):
        self.leftarg.eval(writer)
        self.rightarg.eval(writer)
        self.id = IdGenerator.getNextId()
        writer.append(self.id + " = " + self.leftarg.id +" "+self.operator+" "+self.rightarg.id)
        
    
    @addToClass(AssignOp)
    def eval(self, writer):
        self.leftarg.eval(writer)
        self.rightarg.eval(writer)
        writer.append(self.leftarg.id + " = " + self.rightarg.id)
        self.id = self.leftarg.id
        
        
    @addToClass(CompOp)
    def eval(self, writer):
        self.leftarg.eval(writer)
        self.rightarg.eval(writer)
        
        self.leftid = self.leftarg.id
        self.rightid = self.rightarg.id
        
    
    @addToClass(While)
    def eval(self, writer):
        conditionStartLine = writer.getLen()
        self.condition.eval(writer) # condition initialization
        conditionCheckLine = writer.reserveLine() #line for checking condition
        self.body.eval(writer) # while body
        writer.append("if== 1 1 "+str(conditionStartLine)) # after body jumpt to condition ^
        afterWhileLine = writer.getLen() # where to jump when condition is false
        writer.putLine(conditionCheckLine, Utils.getIfCond(self.condition, afterWhileLine))
    
    
    @addToClass(If)
    def eval(self, writer):
        self.condition.eval(writer)
        lineno = writer.reserveLine()
        self.ifbody.eval(writer)
        jumpLine = writer.getLen()
        writer.putLine(lineno, Utils.getIfCond(self.condition, jumpLine))
        
        
    @addToClass(IfElse)
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
        
        
    @addToClass(Constant)
    def eval(self, writer):
        pass
    
    
    @addToClass(Variable)
    def eval(self, writer):
        pass
    

    # @addToClass(InstList)
    # def eval(self):
        # raise Exception("eval not defined in class " + self.__class__.__name__);


    #@addToClass( ... )
    #def eval(self):
    # ...

'''
 ______   ______     ______     ______     ______     ______    
/\  == \ /\  __ \   /\  == \   /\  ___\   /\  ___\   /\  == \   
\ \  _-/ \ \  __ \  \ \  __<   \ \___  \  \ \  __\   \ \  __<   
 \ \_\    \ \_\ \_\  \ \_\ \_\  \/\_____\  \ \_____\  \ \_\ \_\ 
  \/_/     \/_/\/_/   \/_/ /_/   \/_____/   \/_____/   \/_/ /_/ 
                                                                
                                                                '''


literals = "{}()<>=;,+-*/"


tokens = ( "ID", "FLOAT", "INTEGER", "STRING",
        "TYPE", "IF", "ELSE", "WHILE", "EQ", "NEQ", "LE", "GE" );


t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


def t_FLOAT(t):
    r"\d+(\.\d*)|\.\d+"
    return t

def t_INTEGER(t):
    r"\d+"
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_IF(t):
    r"if"
    return t

def t_ELSE(t):
    r"else"
    return t

def t_WHILE(t):
    r"while"
    return t

def t_LE(t):
    r"<="
    return t

def t_GE(t):
    r">="
    return t

def t_EQ(t):
    r"=="
    return t

def t_NEQ(t):
    r"!="
    return t

def t_TYPE(t):
    r"int|float|string"
    return t

def t_ID(t):
    r"[a-zA-Z_]\w*"
    return t


precedence = (
("nonassoc", 'IFX'),
("nonassoc", 'ELSE'),
("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
("left", '+', '-'),
("left", '*', '/') )



def p_error(p):
    print("Syntax error at token", p.type)

def p_program(p):
    """program : declarations instructions"""
    p[0] = (p[1], p[2])

def p_declarations(p):
    """declarations : declarations declaration 
                    | """
    if len(p) == 1:
        p[0] = Declarations()
    else:
        p[1].sum(p[2], p.lexer.lineno)
        p[0] = p[1]
     

def p_declaration(p):
    """declaration : TYPE vars ';' """
    declarations = Declarations()
    for v in p[2]:
        declarations.append(v.name , p[1], p.lexer.lineno)
    p[0] = declarations
    

def p_vars(p):
    """vars : vars ',' ID
            | ID """
    if len(p) > 3:
        p[1].append(Variable(p[3], p.lexer.lineno))
        p[0] = p[1]
    else:
        p[0] = [Variable(p[1], p.lexer.lineno)]

def p_instructions(p):
    """instructions : instructions instruction
                    | instruction"""
    if len(p) == 2:
        inst = InstList()
        inst.append(p[1])
        p[0] = inst
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_instruction(p):
    """instruction : assignment
                | choice_instr
                | while_instr """
    p[0] = p[1]

def p_assignment(p):
    """assignment : ID '=' expression ';' """
    p[0] = AssignOp(Variable(p[1], p.lexer.lineno), p[3], p.lexer.lineno)

def p_expression_id(p):
    """expression : ID """
    p[0] = Variable(p[1], p.lexer.lineno)
    
def p_expression_const(p):
    """expression : const """      
    p[0] = p[1];
  
def p_expression_bra(p):
    """expression : '(' expression ')' """   
    p[0] = p[2]
                
def p_arithm_expression(p):
    """expression : expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression"""

    p[0] = ArithmOp(p[2], p[1], p[3], p.lexer.lineno)

def p_const_int(p):
    """const : INTEGER"""
    p[0] = Constant(p[1], INT_TYPE, p.lexer.lineno);
    
def p_const_flo(p):
    """const :  FLOAT"""
    p[0] = Constant(p[1], FLOAT_TYPE, p.lexer.lineno);
    
def p_const_str(p):
    """const : STRING"""
    p[0] = Constant(p[1], STRING_TYPE, p.lexer.lineno);

def p_choice_instr1(p):
    """choice_instr : IF '(' condition ')' stmt %prec IFX """
    p[0] = If(p[3], p[5], p.lexer.lineno)

    
def p_choice_instr2(p):
    """choice_instr : IF '(' condition ')' stmt ELSE stmt """
    p[0] = IfElse(p[3], p[5], p[7], p.lexer.lineno)

def p_while_instr(p):
    """while_instr : WHILE '(' condition ')' stmt """
    p[0] = While(p[3], p[5], p.lexer.lineno)

def p_condition(p):
    """condition : expression EQ  expression
                | expression NEQ expression
                | expression GE  expression
                | expression LE  expression
                | expression '<' expression
                | expression '>' expression """
    p[0] = CompOp(p[2], p[1], p[3], p.lexer.lineno)

def p_stmt(p):
    """stmt : assignment
            | '{' instructions '}'
            | choice_instr
            | while_instr """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

'''
 ____    ____          _            
|_   \  /   _|        (_)           
  |   \/   |   ,--.   __   _ .--.   
  | |\  /| |  `'_\ : [  | [ `.-. |  
 _| |_\/_| |_ // | |, | |  | | | |  
|_____||_____|\'-;__/[___][___||__] 
                                    
                                    '''


file = open(sys.argv[1] if len(sys.argv) > 1 else "example.txt", "r");


lexer = lex.lex()
parser = yacc.yacc()
text = file.read()
(declarations, instructions) = parser.parse(text, lexer=lexer)

types = Types()
if(instructions.check(types, declarations) == types.error()):
    print("Compilation failed.")
    exit()

writer = LineWriter()
instructions.eval(writer)
linesWithNumbers = dict(zip(range(0,writer.getLen()), writer.getLines()))

for i in range(0,writer.getLen()) :
    print(str(i) + ": " + linesWithNumbers[i])
    
#pprint(linesWithNumbers)
#pprint(declarations.dic)


