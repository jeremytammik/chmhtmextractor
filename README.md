# chmhtmextractor
CHM Help File HTML Snippet Content Extractor

## Classification

What classes of objects are described by the 28282 help files?

- E &rarr; event 116
- F &rarr; field 4
- M &rarr; method 8290
- N &rarr; namespace 30
- P &rarr; property 12848
- R &rarr; root? 1
- T &rarr; type 2686
- Overload &rarr; overload 603

```
% sed "s/^.*[\.\:]\(.\)\:.*$/\1/" title_helpid_list.txt | sort | uniq | grep -v Overload
1593f994-fb7b-4b7d-ae1d-1c0ba3337577.htm:Major changes and renovations to the Revit API:1593f994-fb7b-4b7d-ae1d-1c0ba3337577
2db849bc-e193-4919-a96c-cc324cf06f66.htm:Migrating From .NET 4.8 to .NET 8:2db849bc-e193-4919-a96c-cc324cf06f66
E
F
M
N
P
R
T```
