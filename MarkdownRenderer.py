import mistune
import pygments.util
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.HTMLRenderer):
    def heading(self, text: str, level: int):
        tag = 'h' + str(level)
        anchor = f"<a href='{text.lower().replace(' ', '-')}'></a>"
        return anchor + '<' + tag + '>' + text + '</' + tag + '>\n'
    def block_code(self, code, lang=None, info=None):
        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except pygments.util.ClassNotFound:
                return '<pre><code>' + mistune.escape(code) + '</code></pre>'
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'
