```
┌─┐┌─┐┌─┐┬┌─┌─┐┌┬┐
│  │ ││ │├┴┐├┤  ││
└─┘└─┘└─┘┴ ┴└─┘─┴┘
the cooked programming language
```
## Table of Contents
[What is cooked?](#what-is-cooked) \
[Structure of the project](#structure-of-the-project) \
[Usage](#usage) \
[VSCode Syntax](#vscode-syntax)
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

## VSCode Syntax
As always, I provide syntax highlighting for VSCode. Simply do the following:
- Ctrl/Command + Shift + P
- Choose 'Developer: Install Extension from Location'
- Select the vscode-syntax folder