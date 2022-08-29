def help():
    """Provide help message listing commands"""
    help_messages = {
        "help": "display this message",
        "init": "initialise directory for victor project",
        "build": "build directory",
        "serve [PORT]": "start basic web server at port, default is 8000",
        "new FILE": "create a new file with content of archetype"
    }
    print("Available commands:")
    # Whitespace between command and description
    col_gap = 16
    for command in help_messages.keys():
        print(f"  {command}{' ' * (col_gap - len(command))}{help_messages[command]}")