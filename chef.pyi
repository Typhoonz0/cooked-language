"""
chef.pyi
........
Interface file to show the argument and return types of chef.py.
Hover over a function in your IDE and it will show you the function.
"""

class ASTNode:
    """
    Base class for all AST nodes.
    - Provides a default compile() method that returns an empty string.
    - All node types should inherit from this class.
    """
    def compile(self) -> str: ...

class VariableBlock(ASTNode):
    """
    - Represents a block that defines variables using the $vars syntax.
    - Stores variables in a dictionary and updates the context during compilation.
    - Produces no HTML output itself.
    """
    def __init__(self, assignments: str) -> None: ...
    def compile(self, context: str) -> str: ...


class Parser:
    """ 
    - Parses the raw input source text into an Abstract Syntax Tree (AST) <br>
    - Detects both $vars blocks and named tag blocks <br>
    - Each block becomes an instance of VariableBlock or TagBlock <br>
    """
    def __init__(self, source: str, debug: bool) -> None: ...

    def parse(self) -> list: ...
    """ 
    - Uses a regular expression to find all blocks in the source <br>
    - Returns a list of ASTNode instances (VariableBlock and TagBlock) <br>
    """
    
    def parseWithAttrs(self, tag_raw: str) -> tuple: ...
    """
    - Parses tag names and attributes from:
    'a href="link"'
    'a href=//github.com'
    - Attributes may be quoted or unquoted. 
    """
        
    def _parse_vars(self, lines: str) -> dict: ...
    """
    - Parses lines from a $vars block
    - Extracts variable assignments of the form key = 'value'
    - Returns a dictionary of variable names and their values
    """

class TagBlock:
    """
    - Represents a generic HTML block (e.g., head, body, section, div) <br>
    - Supports optional attributes (class, id) parsed from tag headers <br>
    """
    def __init__(self, tag_name: str, content_lines:list, attributes: dict = None) -> None: ...

    def compile(self, context: dict) -> str: ...
    """
    Compiles the abstract syntax into valid HTML. <br>
    First finds and compiles attributes, then div blocks, then returns valid HTML. <br>
    """

    def _compileNested(self, line: str, context: dict) -> str:
        """
        Recursively compiles lines with nested tags like:
        a href="link": Text
        Returns final HTML string.
        As you can tell by the nested code below, this was not fun.
        """

        def isQuoted(s: str) -> bool: ...
        """
        Self explanatory, returns True if the string is quoted.
        We don't need to make this local since the function is already nested within a local function.
        """

        def findColon(s: str) -> str: ...
        """
        - Because we use colons as an operator instead of <tag></tag>'ing content, 
        we need to see where the colons are otherwise when using colons in a regular context, 
        e.g. a URL, it will attempt to end the tag instead of parsing as a literal.
        Making these helper functions like this and the one above is a lot easier to read, even though I hate nested functions.
        """
            
    def parseWithAttrs(self, tag_raw: str) -> tuple: ...
    """
    Parses tag names and attributes from lines like:
    'a href="link"' or 'a href=//github.com'
    """

    def interpolate(self, text: str, context: dict) -> str: ...
    """
    - Replaces $variables with their values from context
    """

class Compiler:
    """
    - Walks through the AST and compiles it into a valid HTML string
    - Maintains a context dictionary for resolving $variables
    """
    def __init__(self, ast: dict, debug: bool) -> None: ...
    def compile(self) -> str: ...
