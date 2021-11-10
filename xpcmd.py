#!/usr/bin/python

# --- INITIALIZATION

import getopt
import sys

from outputters import MyErrorHandler
from xmlproc import xmlproc
from xmlproc.namespace import NamespaceFilter
from xmlproc.utils import ESISDocHandler, Canonizer, DocGenerator

"""
A command-line interface to the xmlproc parser. It continues parsing
even after fatal errors, in order to be find more errors, since this
does not mean feeding data to the application after a fatal error
(which would be in violation of the spec).
"""

usage = \
    """
    Usage:

      xpcmd.py [options] [urltodoc]

      ---Options:
      -l language: ISO 3166 language code for language to use in error messages
      -o format:   Format to output parsed XML. 'e': ESIS, 'x': canonical XML
                   and 'n': normalized XML. No data will be output if this
                   option is not specified.
      urltodoc:    URL to the document to parse. (You can use plain file names
                   as well.) Can be omitted if a catalog is specified and contains
                   a DOCUMENT entry.
      -n:          Report qualified names as 'URI name'. (Namespace processing.)
      --nowarn:    Don't write warnings to console.
      --entstck:   Show entity stack on errors.
      --extsub:    Read the external subset of documents.
    """


try:
    (options, sysids) = getopt.getopt(sys.argv[1:], "l:o:n",
                                      ["nowarn", "entstck", "rawxml", "extsub"])
except getopt.error as e:
    print("Usage error: " + e)
    print(usage)
    sys.exit(1)

pf = None
namespaces = False
app = xmlproc.Application()
warnings = True
entstack = False
rawxml = False
extsub = False

p = xmlproc.XMLProcessor()

for option in options:
    if option[0] == "-l":
        try:
            p.set_error_language(option[1])
        except KeyError:
            print("Error language '%s' not available" % option[1])
    elif option[0] == "-o":
        if option[1] == "e" or option[1] == "E":
            app = ESISDocHandler()
        elif option[1] == "x" or option[1] == "X":
            app = Canonizer()
        elif option[1] == "n" or option[1] == "N":
            app = DocGenerator()
        else:
            print("Error: Unknown output format " + option[1])
            print(usage)
    elif option[0] == "-n":
        namespaces = True
    elif option[0] == "--nowarn":
        warnings = False
    elif option[0] == "--entstck":
        entstack = True
    elif option[0] == "--rawxml":
        rawxml = True
    elif option[0] == "--extsub":
        extsub = True

# Acting on option settings

err = MyErrorHandler(p, warnings)
p.set_error_handler(err)

if namespaces:
    nsf = NamespaceFilter(p)
    nsf.set_application(app)
    p.set_application(nsf)
else:
    p.set_application(app)

if len(sysids) == 0:
    print("You must specify a file to parse")
    print(usage)
    sys.exit(1)

if extsub:
    p.set_read_external_subset(extsub)

# --- Starting parse

print("xmlproc version %s" % xmlproc.version)

for sysid in sysids:
    print()
    print("Parsing '%s'" % sysid)
    p.set_data_after_wf_error(0)
    p.parse_resource(sysid)
    print(f"Parse complete, {len(err.errors)} error(s)")

    if warnings:
        print(f"and {len(err.warnings)} warning(s)")
    else:
        print()

    err.reset()
    p.reset()
