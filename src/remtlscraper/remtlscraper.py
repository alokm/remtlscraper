import argparse

parser = argparse.ArgumentParser()

title="Command line utility for downloading pdf docs on contamination data"

parser = argparse.ArgumentParser(description=title)
parser.add_argument('-g', action='store', metavar='MRC',
                    dest='mrc_code', type=int, nargs ='+',
                    help='MRC code for region or municipality')
parser.add_argument('-l', '--list', action='store_true', default=False,
                    dest='listflag',
                    help='list available MRC codes')
parser.add_argument('--version', action='version', version='%(prog)s 1.0',
                    help='last updated 2011-12-23 by Alok Mohindra')

results = parser.parse_args()
print 'mrc_codes   =', results.mrc_code
print 'list   =', results.listflag
print '-' * 30

if results.listflag == True:
    print 'show the list of mrc codes'
elif results.mrc_code is not None:
    print 'user specified the following codes:'
    print results.mrc_code
else:
    print 'help what to do?'

