from datetime import datetime
import pathlib
import mistune

class MarkdownDocument:
    """Stores content and metadata of a markdown document"""
    def __init__(self, path: pathlib.Path, markdown: str, metadata: dict):
        """Constructor
        :param content: markdown of document
        :param metadata dictionary of metadata from markdown yaml header

        Accepted metadata Fields:

        * title: title of document
        * date: date of document creation
        * featuredImage: path to find featured_image
        * author
        * rssFullText: whether to include whole text in rss or just description
        * categories: list of categories a document falls under
        * description
        """
        self.path = path
        self.title = metadata["title"]
        self.featured_image = metadata["featuredImage"]
        # Add featured image and title to top of post
        featured_image = f"<img class='post-hero' src='{self.featured_image}' alt='{self.title}'/>" if self.featured_image != "" and \
                                                                                     self.featured_image is not None else ""
        self.markdown = markdown
        self.html = featured_image + f"<h1 class='post-title'>{self.title}</h1>" + mistune.markdown(self.markdown, escape=False)
        self.author = metadata["author"]
        try:
            self.date = metadata["date"]
        except:
            self.date = datetime.now()

        try:
            self.rss_full_text = metadata["rssFullText"]
        except KeyError:
            self.rss_full_text = True
        try:
            self.categories = metadata["categories"]
        except KeyError:
            self.categories = []

        desc_length = 280 if len(self.markdown) > 280 else len(self.markdown)
        self.description = ''.join([char for char in self.markdown[:desc_length] if char.isalnum() or char in "\"\'“” .,!?:;()[]/-\r\n"]) + "..."

