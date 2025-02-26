# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import argparse
import os
import sys

# Linode API imports
from linode_api4 import LinodeClient

# Internal Imports
# Import only with "from x import y", to simplify the code.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from yesterdaypy.product import backup
from yesterdaypy.utils import ERRORS, error

PRODUCTS = ["firewall", "linode", "lke", "vpc"]
PRODUCTS_CALL = {
    "firewall": "networking.firewalls",
    "linode": "linode.instances",
    "lke": "lke.clusters",
    "vpc": "vpcs"
}


def main() -> None:
    """"Backup objects to local or Linode Object Storage."""
    client = LinodeClient(token)
    if args.storage is None:
        storage = os.getcwd()
    else:
        storage = args.storage
    for product in args.products:
        backup(product=product, client_call=PRODUCTS_CALL[product],
               client=client, storage=storage, s3_id=s3_id,
               s3_secret=s3_secret, s3_url=s3_url)


parser = argparse.ArgumentParser()
parser.add_argument("--errors", action="store_true",
                    help="Print all error codes and their meaning.")
parser.add_argument("--storage", type=str,
                    help="Storage to save the data.")
parser.add_argument("--products", choices=PRODUCTS, nargs="+", default=PRODUCTS,
                    help="Products to backup.")
args = parser.parse_args()

if args.errors:
    for code in ERRORS:
        print(f"Error {code}: {ERRORS[code]}.")
    sys.exit(0)

if "LINODE_TOKEN" in os.environ:
    token = os.environ["LINODE_TOKEN"]
else:
    error(1)
if "AWS_ACCESS_KEY_ID" in os.environ:
    s3_id = os.environ["AWS_ACCESS_KEY_ID"]
else:
    s3_id = None
if "AWS_SECRET_ACCESS_KEY" in os.environ:
    s3_secret = os.environ["AWS_SECRET_ACCESS_KEY"]
else:
    s3_secret = None
if "AWS_ENDPOINT_URL" in os.environ:
    s3_url = os.environ["AWS_ENDPOINT_URL"]
else:
    s3_url = None


if __name__ == "__main__":
    main()
