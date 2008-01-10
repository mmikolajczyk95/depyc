#!/usr/bin/env python

"""Setup script for the 'decompyle' distribution."""

____revision__ = "$Id: setup.py,v $"

from distutils.core import setup, Extension

setup (name = "decompyle",
       version = "2.3",
       description = "Python byte-code to source-code converter",
       author = "Adal Chiriliuc",
       author_email = "contact@adal.eu.org",
       url = "http://adal.eu.org/decompyle.php",
       packages=['decompyle'],
       scripts=['scripts/decompyle'],
       ext_modules = [Extension('decompyle/marshal_20',
                                ['decompyle/marshal_22_for_20.c'],
                                define_macros=[('MARSHAL_VERSION', 20)]),
                      ]
      )
