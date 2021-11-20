"""Main method"""
import sys

# Program arguments
if len(sys.argv) == 1:
    from .build import build
    build()

elif sys.argv[1] == "init":
    from .init import init
    init()

elif sys.argv[1] == "serve":
    from .serve import serve
    serve()

elif sys.argv[1] == "new":
    from .new import new
    new()
