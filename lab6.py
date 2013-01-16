#!/usr/bin/python

import sys;
import ply.lex as lex;
import ply.yacc as yacc;
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TypeChecker:

    @addToClass(AST.Node)
    def check(self):
        raise Exception("check not defined in class " + self.__class__.__name__);


    #@addToClass( ... )
    #def check(self):
    # ...


class CodeGenerator:

    @addToClass(AST.Node)
    def eval(self):
        raise Exception("eval not defined in class " + self.__class__.__name__);


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

def p_declarations(p):
    """declarations : declarations declaration 
                    | """

def p_declaration(p):
    """declaration : TYPE vars ';' """

def p_vars(p):
    """vars : vars ',' ID
            | ID """

def p_instructions(p):
    """instructions : instructions instruction
                    | instruction"""
    

def p_instruction(p):
    """instruction : assignment
                   | choice_instr
                   | while_instr """
    

def p_assignment(p):
    """assignment : ID '=' expression ';' """

def p_expression(p):
    """expression : ID
                  | const
                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | '(' expression ')' """


def p_const(p):
    """const : INTEGER
             | FLOAT
             | STRING"""


def p_choice_instr(p):
    """choice_instr : IF '(' condition ')' stmt %prec IFX
                    | IF '(' condition ')' stmt ELSE stmt """

def p_while_instr(p):
    """while_instr : WHILE '(' condition ')' stmt """

def p_condition(p):
    """condition : expression EQ  expression
                 | expression NEQ expression
                 | expression GE  expression
                 | expression LE  expression
                 | expression '<' expression
                 | expression '>' expression """

def p_stmt(p):
    """stmt : assignment
            | '{' instructions '}'
            | choice_instr
            | while_instr """



file = open(sys.argv[1] if len(sys.argv) > 1 else "example.txt", "r");


lexer = lex.lex()
parser = yacc.yacc()
text = file.read()
parser.parse(text, lexer=lexer)




