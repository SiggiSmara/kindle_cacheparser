# kindle cache parser
Parsing the kindle cache xml into something more useful.

## Assumptions

You are running this script on a windows machine.
You have an up to date kindle cache on your windows machine.
You are running python >= 3.9

## How to run it

If you haven't installed the requirements do so now. `pip install -r requirements.txt`

Once requirements are installed you can simply run `python parseme.py --help` to get more information.

The script will write a csv with the kindle cache content it finds in
the xml. The name of the csv will be kindlecache.csv in the same folder you are running your script in.


