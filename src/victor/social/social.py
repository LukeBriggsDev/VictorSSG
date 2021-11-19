import os
from enum import Enum


class SocialSite:
    def __init__(self, url: str, account_prefix: str, fa_logo: str):
        """Constructor

        :param url: base url for site e.g twitter.com
        :param account_prefix: the url for an account e.g linkedin.com/in/
        :param fa_logo: name of logo in <a href="https://fontawesome.com"> font-awesome </a> e.g fa-linkedin
        """
        self.url = url
        self.account_prefix = account_prefix
        self.logo = fa_logo


class SocialLink:
    def __init__(self, site: SocialSite, username: str):
        """Constructor

        :param site: SocialSite the link is for
        :param username: username of account
        """
        self.site = site
        self.username = username
        self.link = site.account_prefix + self.username


class DefaultSites:
    """Social sites

    Supported Sites:

    * LINKEDIN
    * GITHUB
    * GITLAB
    * TWITTER
    """
    LINKEDIN = SocialSite("linkedin.com", "linkedin.com/in/", "fa-linkedin")
    GITHUB = SocialSite("github.com", "github.com/", "fa-github")
    GITLAB = SocialSite("gitlab.com", "gitlab.com/", "fa-gitlab")
    TWITTER = SocialSite("twitter.com", "twitter.com/", "fa-twitter")
