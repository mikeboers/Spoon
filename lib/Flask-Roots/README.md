Flask-Roots
===========

> Root: (noun) The part of a plant that attaches it to the ground or to a support, conveying water and nourishment to the rest of the plant.

A collection of shell scripts and the core of a Flask application to support the common elements of many web apps.

Specifically, this is designed for my own sites, and may be of little use to outsiders.


What Flask-Roots Provides
-------------------------

In no particular order:

- a Flask app with extensions including:
    - Flask-Mako
    - Flask-SQLALchemy
    - Flask-WTForms
    - Flask-WTCrud (in development)
    - Flask-Images (currently Flask-ImgSizer)
- a virtualenv with Ruby and Node package freezing;
- basic logging
- basic error handling
- extensible configuration mechanism;
- HAML templates (triggered via a `.haml` extension);
- slightly more secure sessions;
- a `re` route converter;
- several Markdown extensions;
- CSS processing via SASS;
- Javascript concatenation and minification via Sprockets;
- basic schema migrations partialy by SQLAlchemy-Migrate.


Bootstrapping
-------------

For now, Flask-Roots assumes that you want to operate the web app out of the directory that it is in. All of the run-time information should be stored in `var`, so you can destroy that to start with a clean slate.

