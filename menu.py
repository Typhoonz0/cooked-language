"""
menu
....
A GNU Make clone for the cooked programming language.

# Indicates a comment.
$ Indicates a command to be run in the shell.
Anything else is passed to the comp function.

How to use:
>>> python3 menu.py 
Will select the 'all' target in the Menufile
>>> python3 menu.py custom
Will select the 'custom' target in the Menufile
"""

import sys
sys.dont_write_bytecode = True 
import os
import chef 

def comp(filename: str) -> None:
    # First, read the input file:
    src = open(filename.split()[0]).read()
    # Next, initialize the parser:
    parse = chef.Parser(src, False)
    # Then, parse the input into abstract syntax:
    ast = parse.parse()
    # Next, initialize the compiler:
    compile = chef.Compiler(ast, False)
    # Compile the output into valid HTML:
    output = compile.compile()
    # Finally, write to the output file:
    open(filename.split()[1] if len(filename.split()) > 1 else "output.html", "w").write(output)

def main() -> None: 
    # First, read the Menufile:
    src = []
    if os.path.exists("Menufile"):
        raw_src = open("Menufile").readlines()
        # Remove newline characters:
        [src.append(line.strip()) for line in raw_src]
    else:
        print("Error: No Menufile present in the current working directory.")
        sys.exit(1)

    # Unless specified, skip to the 'all' block:
    if len(sys.argv) < 2:
        target = "all"
    else:
        target = sys.argv[1]

    # Find the block and see where its first empty line is. This gives a range of commands to run:
    stop = len(src)  
    try:
        place = src.index(f"{target}:")
    except: 
        print(f"Error: No target named {target}.")
        sys.exit(1)
        
    for i in range(place + 1, len(src)):
        if src[i] == "":
            stop = i
            break

    # Finally, compile the input files:
    for i in range(place + 1, stop):
        if src[i][0] == "#": 
            continue
        elif src[i][0] == "$": 
            print(src[i][1:])
            os.system(src[i][1:])
        else: 
            print(src[i])
            comp(src[i])

if __name__ == "__main__":
    main()
