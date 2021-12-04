# Victor: Static Site Generator

- [Victor: Static Site Generator](#victor--static-site-generator)
  * [Install](#install)
    + [From source](#from-source)
    + [From TestPyPI](#from-testpypi)
  * [Usage](#usage)
    + [Init](#init)
      - [Archetypes](#archetypes)
        * [Python Templating](#python-templating)
      - [config.yml](#configyml)
      - [Content](#content)
      - [Public](#public)
      - [Static](#static)
    + [New](#new)
    + [Build](#build)
    + [Serve](#serve)
  * [Example images](#example-images)

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

  - `python3 -m pip install --extra-index-url https://test.pypi.org/simple/ --index-url https://pypi.org/simple victor-ssg`

## Usage

### Init
`cd` into an empty directory and initialise

`python3 -m victor init`

This will create the following directory structure

```
.
├── archetypes
│   └── default.md
├── config.yaml
├── content
├── public
└── static
```

#### Archetypes
This folder contains templates for files created using the `new` command.
All files are named `default.ext` where ext is the extension of the new file.

The default archetype is for markdown and looks like this:

```markdown
---
title: ""
date: {{ datetime.now().strftime('%Y-%m-%dT%H:%M:%S') }}
featuredImage: 
author: name
rssFullText: true
categories: []
description:
---
```

It is a YAML header that includes metadata to draw from when rendering the webpage.

`title` - Title of the page, Appears at the top of a page as a level 1 heading. 
Also appears as the title in any list of posts or projects.

`date` - The date of a post or project and determines its order on the page

`featuredImage` - The hero image that appears on the pages that lists posts or projects.
Also appears at the top of any post or project page. Any relative urls are relative to the base_url set in `config.yml`

`author` - The author of the post, used in RSS feed

`rssFullText` - Whether the RSS description should use the whole text or just the descriptioon

`categorites` - A list of categories the post belongs to, currently unused

`description` - A description of the post or project. Used underneath the title in the projects or posts pages,
If a value is missing then a 280 character excerpt is used instead

##### Other options

`includeInSitemap` - By default this is true, setting this to `false` will not include that pag in the sitemap in the built site.

##### Python Templating
You can include python in these archetypes that is ran upon file creation by placing it within jinja style braces:

``{{ python code }}``

#### config.yml
This is a yaml file containing configuration information. 
The default config is as follows:

```yaml
{
  "title": "Title",
  "name": "John Smith",
  "subtitle": "a blog",
  "email": "john@example.com",
  "description": "Blog feed",
  "base_url": "http://example.com/",
  "navbar": [
    {
      "name": "Home",
      "url": ""
    },
    {
      "name":  "Posts",
      "url": "posts"
    },
    {
      "name": "Projects",
      "url": "projects"
    },
    {
      "name": "About",
      "url": "about"
    }
  ],
  "index": {
    "socialLinks" : { # Usernames of social platforms
      "linkedin": "",
      "github": "",
      "gitlab": "",
      "twitter": "",
      "rss": "index.xml",
    }
  },
}
```

`title` - Title of website, used within RSS feed, page title and index page

`name` - Your name, used within RSS feed

`subtitle` - Subtitle that appears next to main title on index page

`email` - Used in RSS feed

`description` - Description of RSS feed

`base_url` - **IMPORTANT** - URL all relative links will be relative to.
For example if a blog post has a markdown link to `myimage.jpg`, this will resolve to `https://www.example.com/myimage.jpg`

`navbar` - list of page links that will appear in the navigation bar

&nbsp;&nbsp;&nbsp;&nbsp; `name` - name of link to appear in nav bar

&nbsp;&nbsp;&nbsp;&nbsp; `url` - url of navigation link

`socialLinks` - Usernames or links of social sites.
For default sites (LinkedIn, Github, etc) you must use your username for that site.
For added sites you must use a URL.
Any non default sites will look for a fontawesome icon for that site.
For example, adding `"facebook"` will use the `fa-facebook` icon

#### Content
The content folder is where markdown files will be created using the `new` command.

Any markdown files in the `content` directory will be converted into HTML files.

The files' path relative to the `content` directory will be their path relative to the base_url on build.

Files added to the `posts` directory will be treated as posts

Files added to the `projects` directory will be treated as projects

Any other markdown files will be converted and added to `public` at the same path they are to `content`

#### Public
The `public` folder is the output directory that your static site will be generated into.

#### Static
Any content in the static folder will be copied as-is into the root of the public directory

### New
To create a new post

`python3 -m victor new posts/first-post.md`

To create a new project page

`python3 -m victor new projects/first-project.md`

To create any other markdown file to be converted

`python3 -m victor new path/file.md`

**There must be at least 1 project and 1 post for the site to build**

### Build

To build the page simply run

`python3 -m victor`

Your static site will be generated in `public`

### Serve

Victor comes with an *incredibly* rudimentary web server:

`python3 -m victor serve`

If you make any changes while the server is running then you will have to close the server, rebuild, then restart the server.

## Example images
![home_page](README_IMAGES/home_page.png)
![post_page](README_IMAGES/post_page.png)
![project_page](README_IMAGES/project_page.png)

There is also an automatic dark theme