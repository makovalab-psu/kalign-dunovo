#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import os
import sys
import errno
import ctypes
import logging
import argparse
import tempfile
PY3 = sys.version_info.major >= 3

# Locate the library file.
LIBFILE = 'libkalign.so'
script_dir = os.path.dirname(os.path.realpath(__file__))
library_path = os.path.join(script_dir, LIBFILE)
if not os.path.isfile(library_path):
  ioe = IOError('Library file "'+LIBFILE+'" not found.')
  ioe.errno = errno.ENOENT
  raise ioe

kalign = ctypes.cdll.LoadLibrary(library_path)


class AlignmentStruct(ctypes.Structure):
  _fields_ = [
    ('nseqs', ctypes.c_int),
    ('seqlen', ctypes.c_int),
    ('names', ctypes.POINTER(ctypes.c_char_p)),
    ('seqs', ctypes.POINTER(ctypes.c_char_p)),
  ]

kalign.align.restype = ctypes.POINTER(AlignmentStruct)


def make_argparser():
  parser = argparse.ArgumentParser(description='Align a set of sequences.')
  parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin, nargs='?',
    help='Input sequences.')
  return parser


def main(argv):
  parser = make_argparser()
  args = parser.parse_args(argv[1:])
  seqs = []
  for line_raw in args.input:
    line = line_raw.rstrip('\r\n')
    if line.startswith('>'):
      continue
    else:
      seqs.append(line)
  alignment = align(seqs)
  for seq in alignment:
    print(seq)


def align(seqs):
  """Perform a multiple sequence alignment on a set of sequences and parse the result."""
  input_file = tempfile.NamedTemporaryFile('w', delete=False, prefix='align.msa.')
  try:
    i = 0
    for seq in seqs:
      i += 1
      input_file.write('>seq{}\n'.format(i))
      input_file.write(seq+'\n')
    input_file.close()
    argc, argv = make_args(input_file.name)
    logging.info('Calling {} with $ {}'.format(LIBFILE, b' '.join(argv)))
    alignment_struct = kalign.align(argc, argv)
    # A possible error the kalign C code can cause is messing up stderr.
    # If you try to write to stderr after this happens, it will raise an IOError (errno 0).
    # If that doesn't happen, the script will continue as normal, but logging to stderr will
    # silently fail.
    if sys.stderr.fileno() == -1:
      logging.error('Error: '+LIBFILE+' borked stderr.')
    return pythonify_alignment(alignment_struct.contents)
  finally:
    # Make sure we delete the temporary file.
    try:
      input_file.close()
    except OSError:
      pass
    try:
      os.remove(input_file.name)
    except OSError:
      pass


def make_args(infile):
  argv_list = ('kalign', infile, '-o', '/dev/null')
  argc = len(argv_list)
  argv_c = strlist_to_c(argv_list)
  return argc, argv_c


def strlist_to_c(strlist):
  c_strs = (ctypes.c_char_p * len(strlist))()
  for i, str_raw in enumerate(strlist):
    if PY3:
      str_bytes = bytes(str_raw, 'utf8')
    else:
      str_bytes = str_raw
    c_strs[i] = ctypes.c_char_p(str_bytes)
  return c_strs


def pythonify_alignment(alignment_struct):
  seqs = []
  for i in range(alignment_struct.nseqs):
    seq_raw = alignment_struct.seqs[i]
    if PY3:
      seq_str = str(seq_raw, 'utf8')
    else:
      seq_str = seq_raw
    seqs.append(seq_str)
  return seqs


if __name__ == '__main__':
  sys.exit(main(sys.argv))
