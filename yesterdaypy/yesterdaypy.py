# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import argparse
import os
import sys

import linode_api4

# Internal Imports
# Import only with "from x import y", to simplify the code.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from yesterdaypy.products import firewall
from yesterdaypy.utils.utils import ERRORS, error

# PRODUCTS = ["firewall", "linode"]
PRODUCTS = ["firewall"]


def backup() -> None:
    """"Backup objects to local or Linode Object Storage."""
    if args.storage is None:
        storage = os.getcwd()
    else:
        storage = args.storage
    for product in args.products:
        eval(f"{product}.backup(storage='{storage}')")


parser = argparse.ArgumentParser()
parser.add_argument("--errors", action="store_true",
                    help="Print all error codes and their meaning.")
parser.add_argument("--storage", type=str,
                    help="storage to save the data.")
parser.add_argument("--products", choices=PRODUCTS, nargs="+", default=PRODUCTS,
                    help="products to backup.")
args = parser.parse_args()

if args.errors:
    for code in ERRORS:
        print(f"Error {code}: {ERRORS[code]}.")
    sys.exit(0)

if "LINODE_TOKEN" in os.environ:
    token = os.environ["LINODE_TOKEN"]
else:
    error(1)


def main() -> None:
    backup()


if __name__ == "__main__":
    main()
