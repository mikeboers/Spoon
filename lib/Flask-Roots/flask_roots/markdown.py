"""

Original taken from:
    http://gregbrown.co.nz/code/githib-flavoured-markdown-python-implementation/

I (mikeboers) have adapted it to work properly. It was only replacing newlines
at the very start of of a blob of text. I also removed the emphasis fixer
cause my markdown does it anyways, and this was screwing up flickr links.

The hash should really be salted.

Github flavoured markdown - ported from
http://github.github.com/github-flavored-markdown/

Usage:

    html_text = markdown(gfm(markdown_text))

(ie, this filter should be run on the markdown-formatted string BEFORE the markdown
filter itself.)

"""

from __future__ import absolute_import

import os
import logging
import re
import cgi

from markdown import Markdown
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension

log = logging.getLogger(__name__)

        

extension_constructors = dict(
    codehilite=lambda: CodeHiliteExtension([('guess_lang', False)])
)


extension_usage_defaults = dict(
    nl2br=True,
    codehilite=True,
    abbr=True,
    footnotes=True,
    fenced_code=True,
)


def markdown(text, _unknown=None, **custom_exts):
    
    if not isinstance(text, unicode):
        text = unicode(str(text), 'utf8')
    
    loaded_extensions = []
    ext_prefs = extension_usage_defaults.copy()
    ext_prefs.update(custom_exts)
    for name, include in ext_prefs.iteritems():
        if include:
            ext = extension_constructors.get(name)
            ext = ext() if ext else name
            loaded_extensions.append(ext)
        
    md = Markdown(extensions=loaded_extensions,
                  safe_mode=False, 
                  output_format='xhtml')
    return md.convert(text)
    

