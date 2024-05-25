<img align="right" src="https://raw.github.com/cliffano/oricat/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/oricat/workflows/CI/badge.svg)](https://github.com/cliffano/oricat/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/oricat/badge.svg)](https://snyk.io/test/github/cliffano/oricat)
[![Published Version](https://img.shields.io/pypi/v/oricat.svg)](https://pypi.python.org/pypi/oricat)
<br/>

Oricat
------

Oricat is a Python CLI for categorising image files by orientation.

Given a folder of images, Oricat will organise those files by orientation into subfolders `landscape`, `portrait`, and `square`.

Installation
------------

    pip3 install oricat

Usage
-----

Categorise images in a folder:

    oricat --input-dir some/input/folder/ --output-dir some/output/folder/

The categorised images will then be moved to:

* `some/output/folder/landscape` for images having landscape orientation
* `some/output/folder/portrait` for images having portrait orientation
* `some/output/folder/square` for images having square orientation

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/oricat/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/oricat/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/oricat/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/oricat/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/oricat/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/oricat/doc/sphinx/index.html)
