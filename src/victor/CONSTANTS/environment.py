from jinja2 import Environment, PackageLoader, select_autoescape

# Jinja environment
jinja_env = Environment(
    loader=PackageLoader("victor"),
    autoescape=select_autoescape()
)