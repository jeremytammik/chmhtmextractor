#!/opt/local/bin/python
# -*- coding: utf-8 -*-
#
# chmhtmextractor.py - open text files from a filename list and extract data from them
# Copyright 2024-11-28 by Jeremy Tammik, Autodesk Inc.
#
import os, re

'''
<html>
<head>
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="Microsoft.Help.SelfBranded" content="true" />
  <meta name="Language" content="en-us" />
  <meta name="Microsoft.Help.Locale" content="en-us" />
  <meta name="Microsoft.Help.TopicLocale" content="en-us" />
  <link rel="shortcut icon" href="../icons/favicon.ico" />
  <link rel="stylesheet" type="text/css" href="../styles/branding.css" />
  <link rel="stylesheet" type="text/css" href="../styles/branding-en-US.css" />
  <script type="text/javascript" src="../scripts/branding.js"></script>
  <title>Autodesk.Revit.DB.Steel Namespace</title>
  <meta name="Title" content="Autodesk.Revit.DB.Steel" />
  <meta name="Microsoft.Help.Id" content="N:Autodesk.Revit.DB.Steel" />
  <meta name="Microsoft.Help.ContentType" content="Reference" />
  <meta name="System.Keywords" content="Autodesk.Revit.DB.Steel namespace" />
  <meta name="Microsoft.Help.F1" content="Autodesk.Revit.DB.Steel" />
  <meta name="container" content="Autodesk.Revit.DB.Steel" />
  <meta name="file" content="9b98b590-ace1-9487-a688-8942d90305f1" />
  <meta name="guid" content="9b98b590-ace1-9487-a688-8942d90305f1" />
  <link rel="stylesheet" type="text/css" href="../styles/branding-Help1.css" />
</head>
<body onload="SetDefaultLanguage('cs');">
<input type="hidden" id="userDataCache" class="userDataStyle" />
<div id="PageHeader" class="pageHeader">Revit 2025 API</div>
<div class="pageBody">
<div id="TopicContent" class="topicContent">
<table class="titleTable">
<tr>
<td class="titleColumn">
<h1>Autodesk.<wbr />Revit.<wbr />DB.<wbr />Steel Namespace</h1>
</td>
</tr>
</table>
<div class="summary"> </div>
<div class="collapsibleAreaRegion">
<span class="collapsibleRegionTitle" onclick="SectionExpandCollapse('IDACA')" onkeypress="SectionExpandCollapse_CheckKey('IDACA', event)" tabindex="0">
<img id="IDACAToggle" class="collapseToggle" src="../icons/SectionExpanded.png" />Classes</span>
</div>
<div id="IDACASection" class="collapsibleSection">
<table id="classList" class="members">
<tr>
<th class="iconColumn"> </th>
<th>Class</th>
<th>Description</th>
</tr>
<tr>
<td>
<img src="../icons/pubClass.gif" alt="Public class" title="Public class" />
</td>
<td>
<a href="911b649a-d108-14a2-dc09-8e97d489c17d.htm">SteelElementProperties</a>
</td>
<td>
This class is used to attach steel fabrication information to various Revit elements.
</td>
</tr>
</table>
</div>
</div>
</div>

<div id="PageFooter" class="pageFooter">
  <div class="feedbackLink">Send comments on this topic to
    <a id="HT_MailLink" href="mailto:revitapifeedback%40autodesk.com?Subject=Revit%202025%20API">Autodesk</a>
  </div>
  <script type="text/javascript">
    var HT_mailLink = document.getElementById("HT_MailLink");
    HT_mailLink.href += ": " + document.title + "\u0026body=" + encodeURIComponent("Your feedback is used to improve the documentation and the product. Your e-mail address will not be used for any other purpose and is disposed of after the issue you report is resolved. While working to resolve the issue that you report, you may be contacted via e-mail to get further details or clarification on the feedback you sent. After the issue you report has been addressed, you may receive an e-mail to let you know that your feedback has been addressed.");
  </script>
</div>
</body>
</html>
'''

tags_to_remove = [
  '<meta http-equiv="X-UA-Compatible" content="IE=edge" />',
  '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />',
  '<meta name="Microsoft.Help.SelfBranded" content="true" />',
  '<meta name="Language" content="en-us" />',
  '<meta name="Microsoft.Help.Locale" content="en-us" />',
  '<meta name="Microsoft.Help.TopicLocale" content="en-us" />',
  '<link rel="shortcut icon" href="../icons/favicon.ico" />',
  '<link rel="stylesheet" type="text/css" href="../styles/branding.css" />',
  '<link rel="stylesheet" type="text/css" href="../styles/branding-en-US.css" />',
  '<script type="text/javascript" src="../scripts/branding.js"></script>',
  '<link rel="stylesheet" type="text/css" href="../styles/branding-Help1.css" />',
  '<div id="PageHeader" class="pageHeader">Revit 2025 API</div>',
  '<input type="hidden" id="userDataCache" class="userDataStyle" />',
  '<script type="text/javascript".*HT_mailLink.*</script>'
  '<div id="PageFooter" class="pageFooter">',
]

filenamelist = '/Users/jta/revit2025apidocs/html/filenames.txt'

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

def extract_title_and_helpid( lines ):
  file_count = 0
  helpid_count = 0
  title_count = 0
  helpid_prefix = '<meta name="Microsoft.Help.Id" content="'
  title_prefix = '<title>'
  helpid_prefix_len = len(helpid_prefix)
  title_prefix_len = len(title_prefix)

  with open("/tmp/title_helpid_list.txt", "w") as g:
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

      g.write(filename + ':' + title + ':' + helpid  + '\n')

      #if 20 < file_count:
      #  break

  print (file_count, 'files processed, with', helpid_count, 'helpids and', title_count, 'titles found.')

def delete_garbage( lines ):
  rx = re.compile('|'.join(map(re.escape, tags_to_remove))) # escape to handle metachars
  print( rx )

  file_count = 0
  size_before = 0
  size_after = 0

  for line in lines:

    filename = line.strip()

    with open(filename) as f:
      data = f.read()

    sizea = len(data)
    data = rx.sub('', data)
    sizeb = len(data)

    file_count += 1

    print(filename, sizea, '-->', sizeb)
    size_before += sizea
    size_after += sizeb

    with open("/tmp/" + filename, "w") as f:
      f.write(data)

    if 20 < file_count:
      break

  print (file_count, 'files processed, size reduced from ', size_before, 'to', size_after, 'bytes.')

def compile_regex_patterns(tags_to_remove):
  """
  Precompile regular expression patterns for efficient tag removal.

  Args:
  tags_to_remove (list): List of complete HTML tags to remove

  Returns:
  dict: Dictionary of compiled regex patterns
  """
  # Separate footer-related tags from simple tags
  simple_tags = [tag for tag in tags_to_remove if 'PageFooter' not in tag and 'footer' not in tag.lower()]

  # Escape special regex characters and create a single regex pattern with pipe
  simple_tags_pattern = '|'.join(re.escape(tag) for tag in simple_tags)

  patterns = {
    'simple_tags': re.compile(simple_tags_pattern, re.IGNORECASE | re.DOTALL),
    'footer_tag': re.compile(
      r'<div\s+[^>]*id\s*=\s*[\'"]PageFooter[\'"][^>]*>.*?</div\s*>',
      re.IGNORECASE | re.DOTALL
    ),
    'script_tags': re.compile(
      r'<script\b[^>]*>.*?</script\s*>',
      re.IGNORECASE | re.DOTALL
    )
  }
  return patterns

def remove_specified_tags(lines, tags_to_remove):
  """
  Remove specified tags from an HTML file using precompiled regex patterns.
  Process multiple HTML files in a list.
  """
  # Precompile regex patterns
  patterns = compile_regex_patterns(tags_to_remove)

  # Create output directory if it doesn't exist
  output_directory = '/tmp/output'
  os.makedirs(output_directory, exist_ok=True)

  file_count = 0
  size_before = 0
  size_after = 0

  for input_file in lines:
    #if 20 < file_count:
    #  break

    input_file = input_file.strip()
    #print(input_file)

    if input_file.endswith('.html') or input_file.endswith('.htm'):
      output_path = os.path.join(output_directory, input_file)

      try:
        with open(input_file, 'r', encoding='utf-8') as file:
          content = file.read()

        size_before += len(content)
        content = patterns['simple_tags'].sub('', content)
        content = patterns['footer_tag'].sub('', content)
        content = patterns['script_tags'].sub('', content)
        size_after += len(content)

        with open(output_path, 'w', encoding='utf-8') as file:
          file.write(content)

        file_count += 1

      except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
      except PermissionError:
        print(f"Error: Permission denied when trying to read {input_file} or write {output_file}.")
      except Exception as e:
        print(f"An unexpected error occurred: {e}")

  print (file_count, 'files processed, size reduced from ', size_before, 'to', size_after, 'bytes.')

def main():
  f = open( filenamelist )
  lines = f.readlines()
  f.close()
  #delete_garbage( lines )
  extract_title_and_helpid( lines )
  #remove_specified_tags(lines, tags_to_remove)

if __name__ == '__main__':
  main()

