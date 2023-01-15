# kindle cache parser
Parsing the kindle cache xml into something more useful.

## Assumptions

You are running this script on a windows machine.
You have an up to date kindle cache on your windows machine.
You are running python >= 3.9

## How to run it

run `python parseme.py path/to/kindle/cache.xml`

The script will write a csv with the kindle cache content it finds in
the xml. The name of the csv will be kindlecache.csv in the same folder you are running your script in.


