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
[Usage](#usage) \
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
```yaml
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
```yaml
$vars {
    name = 'User'
    className = 'container'
}
```

- Access these variables by prefacing them with a $, then the name:
```yaml
h1: Hello, $name
```

### Unique quirks
#### Single Line Tags
- Tags only span a single line, so code like:
```yaml
h1:
a href="google.com": Click to google!
```
- would compile, but will keep `a` the default size instead of h1.
- Instead, place tags inside of each other on a line, like so:
```yaml
h1: a href="google.com": Click to google! 
```

#### Recursive divs (bug)
- Currently, divs will be compiled twice. This doesn't affect the output for the end user but can make the HTML hard to read.

## Structure of the project
#### Cooked is meant to be very modular. The structure is as follows:
- `chef.py` contains the parser and the compiler for all the code.
- `serve.py` is an implementation of a build system. You can modify this file to your liking. 

## Usage
- **Create** a file ending in `.meal`. 
- `cd` to the directory you downloaded Cooked.
- `python3 serve.py input.meal` will **compile** `input.meal` into `output.html`. 
You can specify an output path by adding it as the second argument:
- `python3 serve.py input.meal custom.html` will **compile** `input.meal` into `custom.html`. 

## Syntax Highlighting
I provide custom syntax highlighting for VSCode. Simply do the following:
- Ctrl/Command + Shift + P
- Choose 'Developer: Install Extension from Location'
- Select the vscode-syntax folder

If you don't have VSCode, I find `js` or `yaml` highlighting is decent at highlighting the cooked syntax.
