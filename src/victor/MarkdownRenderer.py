import mistune
import pygments.util
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name


class HighlightRenderer(mistune.HTMLRenderer):
    def link(self, link, text=None, title=None):
        if text is None:
            text = link

        # anchor link not relative
        if link[0] == "#":
            return f'''<a href="javascript:;" onclick="document.location.hash='{link[1:]}';">{text}</a>'''

        s = '<a href="' + self._safe_url(link) + '"'
        if title:
            s += ' title="' + mistune.escape_html(title) + '"'
        return s + '>' + (text or link) + '</a>'

    def heading(self, text: str, level: int):
        tag = 'h' + str(level)
        anchor = f"<a name='{text.lower().replace(' ', '-')}'></a>"
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

class TitleRenderer(mistune.HTMLRenderer):
    """Renderer to not wrap text in p tags"""
    def block_html(self, html):
        if not self._escape:
            return html + '\n'
        return mistune.escape(html) + '\n'

    def block_html(self, html):
        if not self._escape:
            return html + '\n'
        return '' + mistune.escape(html) + '\n'