#!/usr/bin/env python
import os
import sys
import errno
import ctypes
import logging
import argparse
import tempfile

# Locate the library file.
LIBFILE = 'libkalign.so'
script_dir = os.path.dirname(os.path.realpath(__file__))
library_path = os.path.join(script_dir, LIBFILE)
if not os.path.isfile(library_path):
  ioe = IOError('Library file "'+LIBFILE+'" not found.')
  ioe.errno = errno.ENOENT
  raise ioe

kalign = ctypes.cdll.LoadLibrary(library_path)


class AlnStrs(ctypes.Structure):
  _fields_ = [
    ('nseqs', ctypes.c_int),
    ('seqlen', ctypes.c_int),
    ('names', ctypes.POINTER(ctypes.c_char_p)),
    ('seqs', ctypes.POINTER(ctypes.c_char_p)),
  ]

kalign.main.restype = ctypes.POINTER(AlnStrs)


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
  for i in range(alignment.nseqs):
    print alignment.seqs[i]


def align(seqs):
  """Perform a multiple sequence alignment on a set of sequences and parse the result."""
  i = 0
  input_file = tempfile.NamedTemporaryFile('w', delete=False, prefix='align.msa.')
  try:
    for seq in seqs:
      i += 1
      input_file.write('>seq{}\n'.format(i))
      input_file.write(seq+'\n')
    input_file.close()
    argc, argv = make_args(input_file.name)
    logging.info('Calling {} with $ {}'.format(LIBFILE, ' '.join([arg for arg in argv])))
    aln = kalign.main(argc, argv)
    # A possible error the kalign C code can cause is messing up stderr.
    # If you try to write to stderr after this happens, it will raise an IOError (errno 0).
    # If that doesn't happen, the script will continue as normal, but logging to stderr will
    # silently fail.
    if sys.stderr.fileno() == -1:
      logging.error('Error: '+LIBFILE+' borked stderr.')
    return aln.contents
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
  for i, s in enumerate(strlist):
    c_strs[i] = ctypes.c_char_p(s)
  return c_strs


if __name__ == '__main__':
  sys.exit(main(sys.argv))
