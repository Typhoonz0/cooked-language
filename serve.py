"""
serve
.....
Build system implementation using the chef library.
I built it with the library <-> endpoint system so users can create their own implementations for their needs, 
but this example system works decently.

How to use:
>>> python3 serve.py inputfile.meal 
Will generate an file named output.html.
>>> python3 serve.py inputfile.meal customname.html
Will generate an file named customname.html.
"""

import sys
sys.dont_write_bytecode = True 
import chef 

def main():
    # First, read the input file:
    src = open(sys.argv[1]).read()
    # Next, initialize the parser:
    parse = chef.Parser(src, False)
    # Then, parse the input into abstract syntax:
    ast = parse.parse()
    # Next, initialize the compiler:
    compile = chef.HTMLCompiler(ast, False)
    # Compile the output into valid HTML:
    output = compile.compile()
    # Finally, write to the output file:
    open(sys.argv[2] if len(sys.argv) > 2 else "output.html", "w").write(output)

if __name__ == "__main__":
    main()