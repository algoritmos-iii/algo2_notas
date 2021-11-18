import os
import sys
import argparse
from pylint import lint

"""
This scripts lints all files given and exits with status code 1 if pylint score is less
than threshold.

Common uses:

* Lint all python files:
`python scripts/lint.py --threshold 7 $(find . -name '*.py')`

* Lint all staged files:
`python scripts/lint.py --threshold 7 $(git diff --name-only --cached)`


"""

parser = argparse.ArgumentParser(description='Lint application')
parser.add_argument("--threshold", metavar='threshold', type=float, nargs=1, required=True,
                    help='lowest threshold accepted')
parser.add_argument("files", metavar='files', nargs='+', type=str,
                    help="files to be linted")
args = parser.parse_args()
threshold = args.threshold[0]
files = args.files


run = lint.Run(files, do_exit=False)
score = run.linter.stats['global_note']

if score < threshold:
    print("The score is less than threshold " + str(threshold))
    sys.exit(1)
