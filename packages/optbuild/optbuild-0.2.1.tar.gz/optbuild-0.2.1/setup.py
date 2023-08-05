#!/usr/bin/env python

"""optbuild: build command lines for external programs

like optparse but in reverse
"""

__version__ = "0.2.1"

# Copyright 2005-2011 Michael M. Hoffman <mmh1@washington.edu>

from setuptools import setup

doclines = __doc__.splitlines()
name, short_description = doclines[0].split(": ")
long_description = "\n".join(doclines[2:])

url = "http://noble.gs.washington.edu/~mmh1/software/%s/" % name.lower()
download_url = "%s%s-%s.tar.gz" % (url, name, __version__)

classifiers = ["Natural Language :: English",
               "Programming Language :: Python"]

install_requires = ["autolog>=0.2.0", "six"]

setup(name=name,
      version=__version__,
      description=short_description,
      author="Michael M. Hoffman",
      author_email="mmh1@uw.edu",
      url=url,
      download_url=download_url,
      classifiers=classifiers,
      license="GNU GPLv2",
      long_description=long_description,
      package_dir={'': 'lib'},
      py_modules=['optbuild'],
      install_requires=install_requires,
      zip_safe=True
      )
