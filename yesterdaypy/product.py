# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import json
import os
import sys

# Internal Imports
# Import only with "from x import y", to simplify the code.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Linode API imports
from linode_api4 import LinodeClient

from yesterdaypy.utils import error_with_text

# Linode object storage
try:
    import boto3
except:
    pass


def backup(product: str, client_call: str, client: LinodeClient, storage: str,
           s3_id: str, s3_secret: str, s3_url: str, output: bool,
           verbose: bool, debug: bool) -> None:
    """Backup objects"""
    try:
        objects = eval(f"client.{client_call}()")
    except RuntimeError as api_error:
        error_with_text(code=2, text=f"{api_error}")

    if (output or verbose):
        print(f"  Backing up product: {product}")
        print(f"  Number of objects: {len(objects)}")
    object_changes = 0

    if storage.startswith("s3://"):
        bucket = storage[5:]
        linode_obj_config = {
            "aws_access_key_id": s3_id,
            "aws_secret_access_key": s3_secret,
            "endpoint_url": s3_url,
        }
        client = boto3.client("s3", **linode_obj_config)
        for object in objects:
            if (verbose):
                print(f"    Object ID: {object.id}")
                print(f"    Object Label: {object.label}")
            if (debug):
                print(f"##### Object ID: {object.id}")
                print(object._raw_json)
            date = object.updated.strftime("%Y%m%d%H%M%S")
            file_name = f"{object.id}+{date}"
            full_file_name = f"{product}/{file_name}.json"
            try:
                client.head_object(Bucket=bucket, key=full_file_name)
                if (verbose):
                    print("    Object Status: same")
            except:
                file_content = json.dumps(object._raw_json)
                try:
                    client.put_object(Body=file_content, Bucket=bucket, Key=full_file_name)
                    object_changes += 1
                    if (verbose):
                        print("    Object Status: changed")
                except RuntimeError as api_error:
                    error_with_text(code=2, text=f"{api_error}")
    else:
        if not os.path.exists(product):
            os.makedirs(f"{storage}/{product}")
        for object in objects:
            if (verbose):
                print(f"    Object ID: {object.id}")
                print(f"    Object Label: {object.label}")
            if (debug):
                print(f"##### Object ID: {object.id}")
                print(object._raw_json)
            date = object.updated.strftime("%Y%m%d%H%M%S")
            file_name = f"{object.id}+{date}"
            full_file_name = f"{storage}/{product}/{file_name}.json"
            if not os.path.exists(full_file_name):
                with open(full_file_name, "w") as file:
                    json.dump(object._raw_json, file)
                    object_changes += 1
                    if (verbose):
                        print("    Object Status: changed")
            else:
                if (verbose):
                    print("    Object Status: same")
    if (output or verbose):
        print(f"  Number of objects that changed: {object_changes}")
