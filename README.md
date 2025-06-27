```
┌─┐┌─┐┌─┐┬┌─┌─┐┌┬┐
│  │ ││ │├┴┐├┤  ││
└─┘└─┘└─┘┴ ┴└─┘─┴┘
the cooked programming language
```
## Table of Contents
[What is cooked?](#what-is-cooked) \
[Syntax](#syntax-overview) \
[Structure of the project](#structure-of-the-project) \
[Basic Compilation](#serve-usage) \
[Advanced Compilation](#menu-usage) \
[VSCode Syntax](#syntax-highlighting)
## What is cooked?
Cooked is a programming language with a clean syntax for writing HTML. Here's an example:

```yaml
$vars {
    name = 'User'
    className = 'container'
}

head {
    link rel="stylesheet" href="style.css":
    title: Example Website
}

body {
    div class=$className [
        h1: 'Hello $name'
        p: 'Welcome to your dashboard.'
        a href='https://google.com': 'Go to google'
    ]
}
```
This is compiled to:
```html
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="style.css"></link>
    <title>Example Website</title>
  </head>
  <body>
    <div class="container">
      <h1>Hello User</h1>
      <p>Welcome to your dashboard.</p>
      <a href="https://google.com">Go to google</a>
    </div>
  </body>
</html>
```

## Syntax Overview
### Declaring tags
- HTML uses tags to structure content on the page.
- Cooked renders tags once on each line instead of closing the tag, like so:
```js
h1: Hello World
```
- Which will compile to:
```html
<h1>Hello World</h1>
```
### Comments
- Comment your cooked code by using two slashes, like so:
```js
// This is a comment. It will be ignored by the compiler.
body {
  h1: "Hello World" 
}
```
### Variables
- Unlike HTML, cooked supports variable assignment. 
- Declare variables by making a $vars block at the top of your file.
```bash
$vars {
    name = 'User'
    className = 'container'
}
```

- Access these variables by prefacing them with a $, then the name:
```bash
h1: Hello, $name
```

### Unique quirks
#### Single Line Tags
- Tags only span a single line, so code like:
```js
h1:
a href="google.com": Click to google!
```
- would compile, but will keep `a` the default size instead of h1.
- Instead, place tags inside of each other on a line, like so:
```js
h1: a href="google.com": Click to google! 
```

#### Recursive nested divs (bug)
- Currently, nested divs will be compiled twice. This doesn't affect the output for the end user but can make the HTML hard to read.

## Structure of the project
#### Cooked is meant to be very modular. The structure is as follows:
- `chef.py` contains the parser and the compiler for all the code.
- `serve.py` is a frontend to `chef.py`. It provides a way to retrive input and output code.
- `menu.py` is a GNU Make-like clone and is more feature-rich than `serve.py`.

## Serve Usage
- To compile files, you will need a program that 'serves' as a frontend to the chef compiler.
- Serve does just this.
- Run in the terminal:
```bash
python3 serve.py inputfile.meal outputfile.html
```
- Running Serve without an output path is the equivalent of:
```bash
python3 serve.py input.meal output.html
```

## Menu Usage
- Menu is a build system used to make compiling multiple projects easier by reading a simple script and executing its instructions.
- It shares the syntax of GNU Make. 
- Create a file named `Menufile` in the same directory as `menu.py`.
- Its structure is simple:
```make
# Hashtags are comments.
all:
  # By default, the 'all' target will be selected first.
  # Targets are seperated by a blank line.
  # This will compile website and divs into HTML with one command!
  tests/website.meal website.html
  tests/divs.meal divs.html

just-website:
  tests/website.meal website.html

clean:
  # Don't want to keep deleting files over and over again?
  # Just run the 'rm' command in your shell. 
  # Shell commands start with a lone dollar sign.
  $ rm -i website.html divs.html
```
- Then, run in the terminal:
```bash
python3 menu.py 
```
- Running the script with no arguments is the equivalent of:
```bash
python3 menu.py all
```

## Syntax Highlighting
I provide custom syntax highlighting for VSCode. Simply do the following:
- Ctrl/Command + Shift + P
- Choose 'Developer: Install Extension from Location'
- Select the vscode-syntax folder

If you don't have VSCode, I find `js` or `yaml` highlighting is decent at highlighting the cooked syntax.