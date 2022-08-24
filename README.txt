Write a simple LISP (expression) parser, following this EBNF grammar:
    expression  = atom | compound ;
    compound    = '(', expression, { whitespace, expression }, ')' |
                  '[', expression, { whitespace, expression }, ']' ;
    whitespace  = ( ' ' | ? newline ? ), { ' ' | ? newline ? } ;
    atom        = literal | identifier ;
    literal     = number | string | bool ;
    nonzero    = '1' | '2' | '3' | '4' |
                 '5' | '6' | '7' | '8' | '9' ;
    digit      = '0' | nonzero ;
    sign       = '+' | '-' ;
    digits     = '0' | ( nonzero, { digit } ) ;
    number     = [ sign ], digits, [ '.', { digit } ] ;
    bool       = '#f' | '#t' ;
    string     = '"', { str_char }, '"' ;
    str_lit    = ? any character except '"' and '\' ? ;
    str_esc    = '\"' | '\\' ;
    str_char   = str_lit | str_esc ;
    identifier = id_init, { id_subseq } | sign ;
    id_init    = id_alpha | id_symbol ;
    id_symbol  = '!' | '$' | '%' | '&' | '*' | '/' | ':' | '<' |
                 '=' | '>' | '?' | '_' | '~' ;
    id_alpha   = ? alphabetic character ?
    id_subseq  = id_init | digit | id_special ;
    id_special = '+' | '-' | '.' | '@' | '#' ;
Alphabetic characters are those for which ‹isalpha()› returns
‹True›. For the semantics of (ISO) EBNF, see e.g. wikipedia.
The parser should be implemented as a toplevel function called
‹parse› that takes a single ‹str› argument. If the string does not
conform to the above grammar, return ‹None›. Assuming ‹expr› is a
string with a valid expression, the following should hold about
‹x = parse(expr)›:
 • an ‹x.is_foo()› method is provided for each of the major
   non-terminals: ‹compound›, ‹atom›, ‹literal›, ‹bool›, ‹number›,
   ‹string› and ‹identifier› (e.g. there should be an ‹is_atom()›
   method), returning a boolean,
 • if ‹x.is_compound()› is true, ‹len(x)› should be a valid
   expression and ‹x› should be iterable, yielding sub-expressions
   as objects which also implement this same interface,
 • if ‹x.is_bool()› is true, ‹bool(x)› should work,
 • if ‹x.is_number()› is true, basic arithmetic (‹+›, ‹-›, ‹*›,
   ‹/›) and relational (‹<›, ‹>›, ‹==›, ‹!=›) operators should
   work (e.g.  ‹x < 7›, or ‹x * x›) as well as ‹int(x)› and
   ‹float(x)›,
 • ‹x == parse(expr)› should be true (i.e. equality should be
   extensional),
 • ‹x == parse(str(x))› should also hold.
If a numeric literal ‹x› with a decimal dot is directly converted to
an ‹int›, this should behave the same as ‹int( float( x ) )›. A few
examples of valid inputs (one per line):
    (+ 1 2 3)
    (eq? [quote a b c] (quote a c b))
    12.7
    (concat "abc" "efg" "ugly \"string\"")
    (set! var ((stuff) #t #f))
    (< #t #t)
Note that ‹str(parse(expr)) == expr› does «not» need to hold.
Instead, ‹str› should always give a canonical representation,
e.g. this must hold:
    str( parse( '+7' ) ) == str( parse( '7' ) )