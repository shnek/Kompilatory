from plyplus import Grammar, STransformer

json_grammar = Grammar(r"""
@start : program;
program : declarations fundefs instructions ;
@declarations : declaration ;
@declaration : TYPE inits ;
@inits : init ;
@init : condition '=' expression ;
@instructions : instruction ;
instruction : print_instr ;


@print_instr : PRINT expression ;

@condition : expression ;
@const : INTEGER | FLOAT ;

@expression : const ;
@expression : expression '+' expression ;

@fundefs : fundef fundefs | fundef ;
@fundef : TYPE '(' args_list_or_empty ')' ;

@args_list_or_empty : args_list;
@args_list : args_list ',' arg ;
@args_list : arg ;
@arg : TYPE ;

TYPE : 'type' ;
PRINT : 'print' ;
INTEGER : 'int' ;
FLOAT : 'float' ;
DOUBLE : 'double';
WHITESPACE : '[ \t\n]+' (%ignore) (%newline);
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