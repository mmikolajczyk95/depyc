#!/usr/bin/env python2
# Mode: -*- python -*-
#
# Copyright (c) 2000-2002 by hartmut Goebel <hartmut@goebel.noris.de>
#
"""
Usage: decompyle [OPTIONS]... [ FILE | DIR]...

Examples:
  decomplye      foo.pyc bar.pyc       # decompyle foo.pyc, bar.pyc to stdout
  decomplye -o . foo.pyc bar.pyc       # decomplye to ./foo.dis and ./bar.dis
  decomplye -o /tmp /usr/lib/python1.5 # decomplye whole library

Options:
  -o <path>     output decompyled files to this path:
                if multiple input files are decompyled, the common prefix
                is stripped from these names and the remainder appended to
                <path>
                  decompyle -o /tmp bla/fasel.pyc bla/foo.pyc
                    -> /tmp/fasel.dis, /tmp/foo.dis
                  decompyle -o /tmp bla/fasel.pyc bar/foo.pyc
                    -> /tmp/bla/fasel.dis, /tmp/bar/foo.dis
                  decompyle -o /tmp /usr/lib/python1.5
                    -> /tmp/smtplib.dis ... /tmp/lib-tk/FixTk.dis
  --verify      compare generated source with input byte-code
                (requires -o)
  --help        show this message

Debugging Options:
  --showasm     include byte-code                  (disables --verify)
  --showast     include AST (abstract syntax tree) (disables --verify)

Extensions of generated files:
  '.dis'             successfully decomplyed (and verified if --verify)
  '.dis_unverified'  successfully decomplyed but --verify failed
  '.nodis'           decompyle failed (contact author for enhancement)
"""

Usage_short = \
"decomyple [--help] [--verify] [--showasm] [--showast] [-o <path>] FILE|DIR..."

import sys, os, getopt
from decompyle import main, verify
import time

showasm = showast = do_verify = 0
outfile = '-'
out_base = None

opts, files = getopt.getopt(sys.argv[1:], 'ho:',
                           ['help', 'verify', 'showast', 'showasm'])
for opt, val in opts:
    if opt in ('-h', '--help'):
        print __doc__
        sys.exit(0)
    elif opt == '--verify':
        do_verify = 1
    elif opt == '--showasm':
        showasm = 1
        do_verify = 0
    elif opt == '--showast':
        showast = 1
        do_verify = 0
    elif opt == '-o':
        outfile = val
    else:
        print Usage_short
        sys.exit(1)

# argl, commonprefix works on strings, not on path parts,
# thus we must handle the case with files in 'some/classes'
# and 'some/cmds'
src_base = os.path.commonprefix(files)
if src_base[-1:] != os.sep:
    src_base = os.path.dirname(src_base)
if src_base:
    sb_len = len( os.path.join(src_base, '') )
    files = map(lambda f: f[sb_len:], files)
    del sb_len
    
if outfile == '-':
    outfile = None # use stdout
elif outfile and os.path.isdir(outfile):
    out_base = outfile; outfile = None
elif outfile and len(files) > 1:
    out_base = outfile; outfile = None

print time.ctime() #, args[0]

try:
    main(src_base, out_base, files, outfile, showasm, showast, do_verify)
except KeyboardInterrupt, OSError:
    pass
except verify.VerifyCmpError:
    raise

print time.ctime()
