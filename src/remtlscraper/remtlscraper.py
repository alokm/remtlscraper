import argparse

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser(description="Command line utility for downloading documentation on air, water, and soil contamination data from public websites")
parser.add_argument('-g', '--get', action='store', metavar='NN',
                    dest='mrc_code', type=int, nargs ='+',
                    help='MRC code for region or municipality')
parser.add_argument('-l', '--list', action='store_true', default=False,
                    dest='listflag',
                    help='list available MRC codes')
parser.add_argument('-u', '--update', action='store_true', default=False,
                    dest='updateflag',
                    help='update list of available MRC codes')
parser.add_argument('-a', '--all', action='store_true', default=False,
                    dest='downloadall',
                    help='download ALL source files for ALL available MRC' +
                         'codes. WARNING: This will download a LOT of data')
parser.add_argument('--version', action='version', version='%(prog)s 1.0',
                    help='last updated 2011-12-23 by Alok Mohindra')

results = parser.parse_args()
print "-" * 24
print 'mrc_code   =', results.mrc_code
print 'list   =', results.listflag
print 'update   =', results.updateflag
print 'all =', results.downloadall
