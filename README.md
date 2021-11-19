# Victor: Static Site Generator
A static site generator for use on my [blog](https://lukebriggs.dev)

This SSG is **rough and unfriendly** and mostly intended just for me. 
There are various features this SSG lacks and it can be strict in how a site should be laid out.
I intend to make it more user-friendly in the future, but for now just treat it as a specialised tool.

You can read more about the background of this SSG on [this post](https://www.lukebriggs.dev/posts/shiny-new-things/#new-site)

## Install
### From source
- Install setuptools and wheel

    - `python3 -m pip install setuptools wheel`

- Create src directory

    - `mkdir $HOME/src`

    - `cd $HOME/src`

- Clone repo

    - `git clone https://github.com/LukeBriggsDev/VictorSSG`

    - `cd VictorSSG`

- Build package

    - `python3 -m build`

- Install package

    - `python3 -m pip install dist/*.tar.gz`

### From TestPyPI
- With pip

  -  `python3 -m pip install --extra-index-url https://test.pypi.org/simple/ --index-url https://pypi.org/simple victor-ssg`