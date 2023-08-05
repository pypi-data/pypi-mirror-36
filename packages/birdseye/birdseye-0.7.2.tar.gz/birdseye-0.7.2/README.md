# ![logo](https://i.imgur.com/i7uaJDO.png) birdseye

[![Build Status](https://travis-ci.org/alexmojaki/birdseye.svg?branch=master)](https://travis-ci.org/alexmojaki/birdseye) [![Supports Python versions 2.7, 3.5, and 3.6](https://img.shields.io/pypi/pyversions/birdseye.svg)](https://pypi.python.org/pypi/birdseye) [![Join the chat at https://gitter.im/python_birdseye/Lobby](https://badges.gitter.im/python_birdseye/Lobby.svg)](https://gitter.im/python_birdseye/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a Python debugger which records the value of expressions in a function call and lets you easily view them after the function exits. For example:

![Hovering over expressions](https://i.imgur.com/rtZEhHb.gif)

Rather than stepping through lines, move back and forth through loop iterations and see how the values of selected expressions change:

![Stepping through loop iterations](https://i.imgur.com/236Gj2E.gif)

See which expressions raise exceptions, even if they're suppressed:

![Exception highlighting](http://i.imgur.com/UxqDyIL.png)

Expand concrete data structures and objects to see their contents. Lengths and depths are limited to avoid an overload of data.

![Exploring data structures and objects](http://i.imgur.com/PfmqZnT.png)

Calls are organised into functions (which are organised into files) and organised by time, letting you see what happens at a glance:

![List of function calls](https://i.imgur.com/5OrB76I.png)

## Integrations with other tools

- [Jupyter/IPython notebooks](#jupyteripython-notebook-integration)

![Jupyter notebook screenshot](https://i.imgur.com/bYL5U4N.png)

- [PyCharm plugin](https://github.com/alexmojaki/birdseye-pycharm)
- [VS Code extension](https://github.com/Almenon/birdseye-vscode/)

## Installation

Simply `pip install birdseye`.

## Usage and features

For a quick demonstration, copy [this example](https://github.com/alexmojaki/birdseye/blob/master/example_usage.py) and run it. Then continue from step 2 below.

To debug your own function, decorate it with `birdseye.eye`, e.g.

```
from birdseye import eye

@eye
def foo():
```

**The `eye` decorator *must* be applied before any other decorators, i.e. at the bottom of the list.**

1. Call the function.
2. Run `birdseye` or `python -m birdseye` in a terminal to run the UI server.
3. Open http://localhost:7777 in your browser.
4. Click on:
    1. The name of the file containing your function
    2. The name of the function
    3. The most recent call to the function

When viewing a function call, you can:

- Hover over an expression to view its value at the bottom of the screen.
- Click on an expression to select it so that it stays in the inspection panel, allowing you to view several values simultaneously and expand objects and data structures. Click again to deselect.
- Hover over an item in the inspection panel and it will be highlighted in the code.
- Drag the bar at the top of the inspection panel to resize it vertically.
- Click on the arrows next to loops to step back and forth through iterations. Click on the number in the middle for a dropdown to jump straight to a particular iteration.
- If the function call you're viewing includes a function call that was also traced, the expression where the call happens will have an arrow (![blue curved arrow](https://i.imgur.com/W7DfVeg.png)) in the corner which you can click on to go to that function call. This doesn't work when calling generator functions.

## Configuration

### Server

```
$ birdseye --help
usage: birdseye [-h] [-p PORT] [--host HOST]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  HTTP port, default is 7777
  --host HOST           HTTP host, default is 'localhost'
```

To run a remote server accessible from anywhere, run `birdseye --host 0.0.0.0`.

### Database

Data is kept in a SQL database. You can configure this by setting the environment variable `BIRDSEYE_DB` to a [database URL used by SQLAlchemy](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls). The default is `sqlite:///$HOME/.birdseye.db`.

If environment variables are inconvenient, you can do this instead:

```python
from birdseye import BirdsEye

eye = BirdsEye('<insert URL here>')
```

You can conveniently empty the database by running:

```bash
python -m birdseye.clear_db
```

## Performance, volume of data, and limitations

Every function call is recorded, and every nontrivial expression is traced. This means that:

- Programs are greatly slowed down, and you should be wary of tracing code that has many function calls or iterations. Function calls are not visible in the interface until they have been completed.
- A large amount of data may be collected for every function call, especially for functions with many loop iterations and large nested objects and data structures. This may be a problem for memory both when running the program and viewing results in your browser.
- To limit the amount of data saved, only a sample is stored. Specifically:
  - The first and last 3 iterations of loops.
  - The first and last 3 values of sequences such as lists.
  - 10 items of mappings such as dictionaries.
  - 6 values of sets.
  - A limited version of the `repr()` of values is used, provided by the [cheap_repr](https://github.com/alexmojaki/cheap_repr) package.
  - Nested data structures and objects can only be expanded by up to 3 levels. Inside loops, this is decreased.

There is no API at the moment to collect more or less data. Suggestions are welcome as it's not obvious how to deal with the problem. But the idea of this tool is to be as quick and convenient as possible and to work for most cases. If in a particular situation you have to think carefully about how to use it, it may be better to use more conventional debugging methods.

Asynchronous code is not supported.

In IPython shells and notebooks, `shell.ast_transformers` is ignored in decorated functions.

## Contributing

I'd love your help! Check out [the wiki](https://github.com/alexmojaki/birdseye/wiki) to get started.

## How it works

The source file of a decorated function is parsed into the standard Python Abstract Syntax Tree. The tree is then modified so that every statement is wrapped in its own `with` statement and every expression is wrapped in a function call. The modified tree is compiled and the resulting code object is used to directly construct a brand new function. This is why the `eye` decorator must be applied first: it's not a wrapper like most decorators, so other decorators applied first would almost certainly either have no effect or bypass the tracing. The AST modifications notify the tracer both before and after every expression and statement. This functionality is generic, and in the future it will be extracted into its own package.

## Jupyter/IPython notebook integration

First, load the birdseye extension, using either `%load_ext birdseye` in a notebook cell or by adding `'birdseye'` to `c.InteractiveShellApp.extensions` in your IPython configuration file, e.g. `~/.ipython/profile_default/ipython_config.py`.

Use the cell magic `%%eye` at the top of a notebook cell to trace that cell. When you run the cell and it finishes executing, a frame should appear underneath with the traced code.

Hovering over an expression should show the value at the bottom of the frame. This requires the bottom of the frame being visible. Sometimes notebooks fold long output (which would include the birdseye frame) into a limited space - if that happens, click the space just left of the output. You can also resize the frame by dragging the bar at the bottom, or click 'Open in new tab' just above the frame.

For convenience, the cell magic automatically starts a birdseye server in the background. You can configure this by settings attributes on `BirdsEyeMagics`, e.g. `%config BirdsEyeMagics.port = 7778` in a cell or `c.BirdsEyeMagics.port = 7778` in your IPython config file. The available attributes are:

- `server_url`: If set, a server will not be automatically started by `%%eye`. The iframe containing birdseye output will use this value as the base of its URL.
- `port`: Port number for the background server.
- `bind_host`: Host that the background server listens on. Set to 0.0.0.0 to make it accessible anywhere. Note that birdseye is NOT SECURE and doesn't require any authentication to access, even if the notebook server does. Do not expose birdseye on a remote server unless you have some other form of security preventing HTTP access to the server, e.g. a VPN, or you don't care about exposing your code and data. If you don't know what any of this means, just leave this setting alone and you'll be fine.
- `show_server_output`: Set to True to show stdout and stderr from the background server.
- `db_url`: The database URL that the background reads from. Equivalent to the environment variable `BIRDSEYE_DB`.
