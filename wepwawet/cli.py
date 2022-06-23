"""
Usage:
  wepwawet (-t TARGET | -f FILE) [-o FILENAME] [-oSv]
  wepwawet -h
  wepwawet (--version | -V)
  
Options:
  -h --help                       show this help message and exit
  -t --target                     set target (comma separated, no spaces, if multiple)
  -f --file                       set target (reads from file, one domain per line)
  -o --output                     save to filename
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

from wepwawet.banner import banner
from wepwawet.utils.convertions import seconds_to_str
from wepwawet.utils.stdouthook import StdOutHook
from wepwawet.utils.color_print import ColorPrint
import wepwawet.commands

from . import __version__ as VERSION

def main():

  try:
    if sys.version_info < (3, 0):
      sys.stdout.write("Sorry, requires Python 3.x\n")
      sys.exit(1)

    start_time = time.time()

    options = docopt(__doc__, version=VERSION)

    print(options)

    if options["--output"] or options["--silent"]:
      sys.stdout = StdOutHook(options["FILENAME"], options["--silent"],
                              options["--output"])

    if not options["--target"] and not options["--file"]:
      ColorPrint.red(
        "Target required! Run with -h for usage instructions. Either -t target.host or -f file.txt required")
      return

    if options["--target"] and options["--file"]:
      ColorPrint.red(
        "Please only supply one target method - either read by file with -f or as an argument to -t, not both.")
      return

    print(banner)

    command = wepwawet.commands.Target(options)
    command.run()

    print("Urls infos search took %s" % seconds_to_str(time.time() - start_time))

    if options["--output"]:
      sys.stdout.write_out()
  except KeyboardInterrupt:
    print("\nQuitting...")
    sys.exit(0)