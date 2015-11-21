from plyplus import Grammar, STransformer

json_grammar = Grammar(r"""
@start : program;


program : declarations fundefs instructions ;

@declarations : declarations declaration | declaration ;
@declaration : TYPE inits ;
@declaration : error ;

@inits : inits ',' init | init ;
@init : ID '=' expression ;

@instructions : instructions instruction | instruction ;
@instruction : print_instr | labeled_instr | assignment | choice_instr | while_instr | repeat_instr | return_instr | break_instr | continue_instr | compound_instr ;

@print_instr : PRINT expression ;
@print_instr : PRINT error ;

@labeled_instr : ID ':' instruction ;
@assignment : ID '=' expression ;

@choice_instr : IF '(' condition ')' instruction ;
@choice_instr : IF '(' condition ')' instruction ELSE instruction ;
@choice_instr : IF '(' error ')' instruction ;
@choice_instr : IF '(' error ')' instruction ELSE instruction ;

@while_instr : WHILE '(' condition ')' instruction ;
@while_instr : WHILE '(' error ')' instruction ;

@repeat_instr : REPEAT instructions UNTIL condition ;
@return_instr : RETURN expression ;

@continue_instr : CONTINUE ;
@break_instr : BREAK ;

@compound_instr : '{' declarations instructions '}' ;
@condition : expression ;
@const : INTEGER | FLOAT | STRING ;

@expression : const ;
@expression : ID ;
@expression : expression '+' expression ;
@expression : expression '-' expression ;
@expression : expression '*' expression ;
@expression : expression '/' expression ;
@expression : expression '%' expression ;
@expression : expression '|' expression ;
@expression : expression '&' expression ;
@expression : expression '^' expression ;
@expression : expression AND expression ;
@expression : expression OR expression ;
@expression : expression SHL expression ;
@expression : expression SHR expression ;
@expression : expression EQ expression ;
@expression : expression NEQ expression ;
@expression : expression '>' expression ;
@expression : expression '<' expression ;
@expression : expression LE expression ;
@expression : expression GE expression ;

@expression : '(' expression ')' ;
@expression : '(' error ')' ;
@expression : ID '(' expr_list_or_empty ')' ;
@expression : ID '(' error ')' ;
@expr_list_or_empty : expr_list ;
@expr_list_or_empty : empty ;

@expr_list : expr_list ',' expression ;
@expr_list : expression ;
@fundefs : fundef fundefs | fundef ;
@fundef : TYPE ID '(' args_list_or_empty ')' compound_instr ;

@args_list_or_empty : args_list | empty ;
@args_list : args_list ',' arg ;
@args_list : arg ;
@arg : TYPE ID ;


empty : 'empty' ;
error : 'error' ;
ID : 'ID' ;

BREAK : 'break' ;
CONTINUE : 'continue' ;
REPEAT : 'repeat' ;
UNTIL : 'until' ;
IF : 'if' ;
ELSE : 'else' ;
TYPE : 'type' ;
PRINT : 'print' ;
RETURN : 'return' ;
INTEGER : 'int' ;
FLOAT : 'float' ;
STRING : 'string' ;
DOUBLE : 'double' ;

WHILE : 'while' ;



GE : '//>=';
LE : '<=';
AND : '&&';
OR : '||';
SHL : '<<';
SHR : '>>';
EQ : '==';
NEQ : '!=';
WHITESPACE: '[ \t\n]+' (%ignore) (%newline);
""")

class Source_Transformer(STransformer):
    """Transforms JSON AST into Python native objects."""
    number  = lambda self, node: float(node.tail[0])
    string  = lambda self, node: node.tail[0][1:-1]
    boolean = lambda self, node: True if node.tail[0] == 'true' else False
    null    = lambda self, node: None
    array   = lambda self, node: node.tail
    pair    = lambda self, node: { node.tail[0] : node.tail[1] }
    def object(self, node):
        result = {}
        for i in node.tail:
            result.update( i )
        return result

def parser_parse(source):
    """Parses a JSON string into native Python objects."""
    return 0;

def main():
    source = '''
float a = 0, b = 0, c = 0;

int gcd(int m, int n) {

int res = 0;
if (m!=n) {
    if (m > n)
        res = gcd(m-n, n);
    else
        res = gcd(n-m, m);
}
else
    res = m;

print res;
return res;
}

while(a >= b ) {
    a = 1/2*(a+b/a);
}
    '''

    print '### Input'
    print source
    print '### Output'
    result = parser_parse(source)
    import pprint
    pprint.pprint(result)

if __name__ == '__main__':
    main()