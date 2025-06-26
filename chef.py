"""
chef
....
The cooking behind the meal programming language. <br>
Actually made: June 16 2025 by Liam <br>
Hover over this library in your IDE (: <br>
I prefer multiline comments as they are green and look nice, so blocks of code will be explained in an overview-like fashion.
Plus, most of this code is self-explanatory and doesn't require excessive comments as they are annoying to edit code with.
"""

import sys, re
sys.dont_write_bytecode = True
RED = "[31m"
CYAN = "[36m"
UNDERLINE = "[4m"
BOLD = "[1m"
RESET = "[0m"

class ASTNode:
    """
    Base class for all AST nodes.
    - Provides a default compile() method that returns an empty string.
    - All node types should inherit from this class.
    """
    def compile(self, context) -> str:
        return ""


class VariableBlock(ASTNode):
    """
    VariableBlock(assignments: dict)
    - Represents a block that defines variables using the $vars syntax.
    - Stores variables in a dictionary and updates the context during compilation.
    - Produces no HTML output itself.
    """
    def __init__(self, assignments) -> None:
        self.assignments = assignments

    def compile(self, context) -> str:
        context.update(self.assignments)
        return ""


class Parser:
    """
    Parser(source: str)
    - Parses the raw input source text into an Abstract Syntax Tree (AST)
    - Detects both $vars blocks and named tag blocks
    - Each block becomes an instance of VariableBlock or TagBlock
    """
    def __init__(self, source, debug) -> None:
        self.source = source
        self.debug = debug

    def parse(self) -> list:
        """
        parse() -> list
        - Uses a regular expression to find all blocks in the source
        - Returns a list of ASTNode instances (VariableBlock and TagBlock)
        """
        ast = []
        """Unholy regular expression - matches non-comment lines, capturing tag names with ascii word args followed by opening bracket, their inner content, and the corresponding closing bracket."""
        blocks = re.findall(
    r'^(?!\s*//)\s*(\$\w+|\w+(?:\s+[^\[{]*)?)\s*(\{|\[)(.*?)(\}|\])',
    self.source,
    re.DOTALL | re.MULTILINE
        )
        for tag_raw, _, content, _ in blocks:
            if self.debug: print(f"Found {RED}block{RESET} with tag {CYAN}{tag_raw}{RESET} with content: {content}")
            lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
            if tag_raw.startswith('$'):
                assignments = self._parse_vars(lines)
                if self.debug: print(f"{CYAN}Parses{RESET} to: ", assignments)
                ast.append(VariableBlock(assignments))
            else:
                tag_name, attributes = self.parseWithAttrs(tag_raw)
                if self.debug:  print(f"{CYAN}Parses{RESET} to:", tag_name, lines, attributes)
                ast.append(TagBlock(tag_name, lines, attributes))
        return ast 

    
    def parseWithAttrs(self, tag_raw: str) -> tuple:
        """
        parseWithAttrs() -> tuple
        - Parses tag names and attributes from:
        'a href="link"'
        'a href=//github.com'
        - Attributes may be quoted or unquoted. 
        """
        parts = []
        buffer = ''
        in_quotes = False
        quote_char = ''

        for c in tag_raw.strip():
            if c in ('"', "'"):
                if in_quotes and c == quote_char:
                    in_quotes = False
                else:
                    in_quotes = True
                    quote_char = c
            if c == ' ' and not in_quotes:
                if buffer:
                    parts.append(buffer)
                    buffer = ''
            else:
                buffer += c

        if buffer:
            parts.append(buffer)

        tag_name = parts[0]
        attributes = {}

        for attr in parts[1:]:
            if '=' in attr:
                key, val = attr.split('=', 1)
                val = val.strip('"\'') 
                attributes[key] = val

        return tag_name, attributes

    def _parse_vars(self, lines) -> dict:
        """
        _parse_vars(lines: list[str]) -> dict
        - Parses lines from a $vars block
        - Extracts variable assignments of the form key = 'value'
        - Returns a dictionary of variable names and their values
        """
        variables = {}
        for line in lines:
            if '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                variables[key] = value.strip("'\"")
        return variables

class TagBlock:
    """
    TagBlock(tag_name: str, content_lines: list, attributes: dict)
    - Represents a generic HTML block (e.g., head, body, section, div)
    - Supports optional attributes (class, id) parsed from tag headers
    """
    def __init__(self, tag_name, content_lines, attributes=None) -> None:
        self.tag_name = tag_name
        self.content_lines = content_lines
        self.attributes = attributes or {}

    def compile(self, context) -> str:
        attr_str = ''.join(
            f' {key}="{self.interpolate(value, context)}"' for key, value in self.attributes.items()
        )
        html = f"<{self.tag_name}{attr_str}>\n"

        i = 0
        while i < len(self.content_lines):
            line = self.content_lines[i].strip()

            if line.endswith('['):
                """
                We need to compile div blocks.
                """
                tag_line = line[:-1].strip()
                tag_name, attrs = self.parseWithAttrs(tag_line)
                attr_str_inner = ''.join(
                    f' {k}="{self.interpolate(v, context)}"' for k, v in attrs.items()
                )
                html += f"<{tag_name}{attr_str_inner}>\n"

                """
                Gather inner lines, handle nested brackets with depth counter.
                """
                inner_lines = []
                depth = 1
                i += 1
                while i < len(self.content_lines) and depth > 0:
                    inner_line = self.content_lines[i].strip()
                    if inner_line.endswith('['):
                        depth += 1
                    elif inner_line == "]":
                        depth -= 1
                        if depth == 0:
                            break
                    inner_lines.append(inner_line)
                    i += 1

                """
                We now use recursion to loop through each div - this creates double divs when no recursion is involved, but that won't affect the end user - just will make it difficult to debug.
                Unless divs or other blocks are explicitly called, clones won't be made, thankfully.
                """
                nested_block = TagBlock(tag_name, inner_lines, attrs)
                html += nested_block.compile(context)

                html += f"</{tag_name}>\n"
            else:
                html += "  " + self._compileNested(line, context) + "\n"

            i += 1

        html += f"</{self.tag_name}>\n"
        return html

    def _compileNested(self, line, context) -> str:
        """
        Recursively compiles lines with nested tags like:
        a href="link": Text
        Returns final HTML string.
        As you can tell by the nested code below, this was not fun.
        """

        def isQuoted(s):
            """
            Self explanatory, returns True if the string is quoted.
            We don't need to make this local since the function is already nested within a local function.
            """
            return (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'"))

        def findColon(s):
            """
            - Because we use colons as an operator instead of <tag></tag>'ing content, 
            we need to see where the colons are otherwise when using colons in a regular context, 
            e.g. a URL, it will attempt to end the tag instead of parsing as a literal.
            Making these helper functions like this and the one above is a lot easier to read, even though I hate nested functions.
            """
            in_single = False
            in_double = False
            for i, c in enumerate(s):
                if c == "'" and not in_double:
                    in_single = not in_single
                elif c == '"' and not in_single:
                    in_double = not in_double
                elif c == ':' and not in_single and not in_double:
                    return i
            return -1

        colon_pos = findColon(line)
        if colon_pos == -1:
            return self.interpolate(line, context)

        tag_part = line[:colon_pos].strip()
        rest = line[colon_pos + 1:].strip()

        if isQuoted(rest):
            """
            If the string is quoted, get rid of the quotes and parse immediately so it doesn't get reparsed incorrectly.
            """
            content = rest[1:-1] 
            content = content.replace('\\"', '"').replace("\\'", "'")
            tag_name, attrs = self.parseWithAttrs(tag_part)
            attr_str = ''.join(
                f' {key}="{self.interpolate(value, context)}"' for key, value in attrs.items()
            )
            return f"<{tag_name}{attr_str}>{self.interpolate(content, context)}</{tag_name}>"

        """
        Otherwise, parse nested tags recursively as usual.
        """

        tag_name, attrs = self.parseWithAttrs(tag_part)
        attr_str = ''.join(
            f' {key}="{self.interpolate(value, context)}"' for key, value in attrs.items()
        )
        inner_html = self._compileNested(rest, context)
        return f"<{tag_name}{attr_str}>{inner_html}</{tag_name}>"

    def parseWithAttrs(self, tag_raw: str) -> tuple:
        """
        Parses tag names and attributes from lines like:
        'a href="link"' or 'a href=//github.com'
        """
        parts = tag_raw.strip().split(None, 1)
        tag_name = parts[0]
        attributes = {}

        if len(parts) > 1:
            attr_text = parts[1]
            matches = re.findall(r'(\w+)=(".*?"|\'.*?\'|\S+)', attr_text)

            for key, val in matches:
                val = val.strip('"\'') 
                attributes[key] = val

        return tag_name, attributes

    def interpolate(self, text, context) -> str:
        """
        interpolate(text: str, context: dict) -> str
        - Replaces $variables with their values from context
        """
        return re.sub(r'\$(\w+)', lambda m: context.get(m.group(1), f"${m.group(1)}"), text)

class HTMLCompiler:
    """
    HTMLCompiler(ast: list)
    - Walks through the AST and compiles it into a valid HTML string
    - Maintains a context dictionary for resolving $variables
    """
    def __init__(self, ast, debug) -> None:
        self.ast = ast
        self.context = {}
        self.debug = debug

    def compile(self) -> str:
        """
        compile() -> str
        - Iterates over all AST nodes and compiles them in order
        - Prepends a <!DOCTYPE html> and wraps everything in <html></html>
        - Returns the final HTML string.
        """
        html = "<!--Compiled with chef.py with the cooked programming language.-->\n<!DOCTYPE html>\n<html>\n"
        for node in self.ast:
            html += node.compile(self.context)
        html += "</html>\n<!--EOF-->"
        return html
