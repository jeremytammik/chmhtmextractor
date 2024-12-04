#!/opt/local/bin/python
# -*- coding: utf-8 -*-
#
# enum_html_help_files.py - open text files from a filename list and extract data from them
# Copyright 2024-11-28 by Jeremy Tammik, Autodesk Inc.

def html_unescape(s):
  """Handle unescape of named HTML characters using htmllib module:
  http://wiki.python.org/moin/EscapingHtml"""
  s = s.replace( '&#324;', 'ñ' ) # not handled by htmllib, apparently
  p = htmllib.HTMLParser(None)
  p.save_bgn()
  p.feed(s)
  s = p.save_end()
  #print s
  return s

def main():
  filenamelist = '/Users/jta/revit2025apidocs/html/filenames.txt'
  f = open( filenamelist )
  lines = f.readlines()
  f.close()

  file_count = 0
  helpid_count = 0
  title_count = 0
  helpid_prefix = '<meta name="Microsoft.Help.Id" content="'
  title_prefix = '<title>'
  helpid_prefix_len = len(helpid_prefix)
  title_prefix_len = len(title_prefix)

  for line in lines:

    filename = line.strip()

    f = open( filename )
    data = f.read()
    f.close()

    helpid = title = '<nil>'

    index = data.find(helpid_prefix)
    if 0 <= index:
      ibegin = index + helpid_prefix_len
      iend = data[ibegin:].find('"')
      helpid = data[ibegin: ibegin + iend]
      helpid_count += 1

    index = data.find(title_prefix)
    if 0 <= index:
      ibegin = index + title_prefix_len
      iend = data[ibegin:].find('<')
      title = data[ibegin: ibegin + iend]
      title_count += 1

    file_count += 1

    print(filename, ':', title, ':', helpid)

    #if 20 < file_count:
    #  break

  print (file_count, 'files processed, with', helpid_count, 'helpids and', title_count, 'titles found.')

if __name__ == '__main__':
  main()
