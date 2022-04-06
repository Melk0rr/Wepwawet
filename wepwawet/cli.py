"""
Usage:
  wepwawet (-t TARGET | -f FILE) [-o FILENAME]
  wepwawet -h
  wepwawet (--version | -V)
  
Options:
  -h --help                       show this help message and exit
  -t --target                     set target (comma separated, no spaces, if multiple)
  -f --file                       set target (reads from file, one domain per line)
  -o --output                     save to filename
  -i --additional-info            show additional information about the host from Shodan (requires API key)
  -S --silent                     only output subdomains, one per line
  -v --verbose                    print debug info and full request output
  -V --version                    show version and exit
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/JaufreLallement/Wepwawet
"""
import sys
import time

from docopt import docopt

from wepwawet.utils.convertions import seconds_to_str
from wepwawet.utils.color_print import ColorPrint

from . import __version__ as VERSION


def main():

  try:
    if sys.version_info < (3, 0):
      sys.stdout.write("Sorry, requires Python 3.x\n")
      sys.exit(1)

    start_time = time.time()

    options = docopt(__doc__, version=VERSION)

    if not options["--target"] and not options['--file']:
      ColorPrint.red(
        "Target required! Run with -h for usage instructions. Either -t target.host or -f file.txt required")
      return

    if options["--target"] and options['--file']:
      ColorPrint.red(
        "Please only supply one target method - either read by file with -f or as an argument to -t, not both.")
      return

    print("""
    888       888                                                                 888    
    888   o   888                                                                 888    
    888  d8b  888                                                                 888    
    888 d888b 888  .d88b.  88888b.  888  888  888  8888b.  888  888  888  .d88b.  888888 
    888d88888b888 d8P  Y8b 888 "88b 888  888  888     "88b 888  888  888 d8P  Y8b 888    
    88888P Y88888 88888888 888  888 888  888  888 .d888888 888  888  888 88888888 888    
    8888P   Y8888 Y8b.     888 d88P Y88b 888 d88P 888  888 Y88b 888 d88P Y8b.     Y88b.  
    888P     Y888  "Y8888  88888P"   "Y8888888P"  "Y888888  "Y8888888P"   "Y8888   "Y888 
                          888                                                           
                          888                                                           
                          888                                                            
    """)

    print("Urls infos search took %s" % seconds_to_str(time.time() - start_time))
  except KeyboardInterrupt:
    print("\nQuitting...")
    sys.exit(0)