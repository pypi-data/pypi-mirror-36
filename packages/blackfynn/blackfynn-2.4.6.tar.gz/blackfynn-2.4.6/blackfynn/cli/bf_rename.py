'''
usage:
  bf rename [options] <item> <new_name>

global options:
  -h --help                 Show help
  --dataset=<dataset>       Use specified dataset (instead of your current working dataset)
  --profile=<name>          Use specified profile (instead of default)
'''

from docopt import docopt
from cli_utils import get_item

from blackfynn.models import BaseDataNode

def main(bf):
    args = docopt(__doc__)

    item = get_item(args['<item>'], bf)
    item.name = args['<new_name>']
    item.update()
