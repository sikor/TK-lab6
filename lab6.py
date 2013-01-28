#!/usr/bin/python

import sys;
import ply.lex as lex;
import ply.yacc as yacc;
from AST import *;
from pprint import pprint;


INT_TYPE = "int"
FLOAT_TYPE = "float"
STRING_TYPE = "str"

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator



class TypeChecker:pass

    # @addToClass(InstList)
    # def check(self):
        # raise Exception("check not defined in class " + self.__class__.__name__);


    #@addToClass( ... )
    #def check(self):
    # ...


class CodeGenerator:pass

    # @addToClass(InstList)
    # def eval(self):
        # raise Exception("eval not defined in class " + self.__class__.__name__);


    #@addToClass( ... )
    #def eval(self):
    # ...


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
        p[1].sum(p[2])
        p[0] = p[1]
     

def p_declaration(p):
    """declaration : TYPE vars ';' """
    declarations = Declarations()
    for v in p[2]:
        declarations.append(v.name , p[1])
    p[0] = declarations
    

def p_vars(p):
    """vars : vars ',' ID
            | ID """
    if len(p) > 3:
        p[1].append(Variable(p[3]))
        p[0] = p[1]
    else:
        p[0] = [Variable(p[1])]

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
    p[0] = AssignOp(Variable(p[1]), p[3])

def p_expression_id(p):
    """expression : ID """
    p[0] = Variable(p[1])
    
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

    p[0] = ArithmOp(p[2], p[1], p[3])

def p_const_int(p):
    """const : INTEGER"""
    p[0] = Constant(p[1], INT_TYPE);
    
def p_const_flo(p):
    """const :  FLOAT"""
    p[0] = Constant(p[1], FLOAT_TYPE);
    
def p_const_str(p):
    """const : STRING"""
    p[0] = Constant(p[1], STRING_TYPE);

def p_choice_instr1(p):
    """choice_instr : IF '(' condition ')' stmt %prec IFX """
    p[0] = If(p[3], p[6])

    
def p_choice_instr2(p):
    """choice_instr : IF '(' condition ')' stmt ELSE stmt """
    p[0] = IfElse(p[3], p[5], p[7])

def p_while_instr(p):
    """while_instr : WHILE '(' condition ')' stmt """
    p[0] = While(p[3], p[5])

def p_condition(p):
    """condition : expression EQ  expression
                | expression NEQ expression
                | expression GE  expression
                | expression LE  expression
                | expression '<' expression
                | expression '>' expression """
    p[0] = CompOp(p[2], p[1], p[3])

def p_stmt(p):
    """stmt : assignment
            | '{' instructions '}'
            | choice_instr
            | while_instr """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


file = open(sys.argv[1] if len(sys.argv) > 1 else "example.txt", "r");


lexer = lex.lex()
parser = yacc.yacc()
text = file.read()
(declarations, instructions) = parser.parse(text, lexer=lexer)
writer = LineWriter()
instructions.eval(writer)
linesWithNumbers = dict(zip(range(0,writer.getLen()), writer.getLines()))

pprint(linesWithNumbers)
pprint(declarations.dic)


