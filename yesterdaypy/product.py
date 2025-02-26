# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
import json
import os

# Linode API imports
from linode_api4 import LinodeClient

# Linode object storage
try:
    import boto3
except:
    pass


def backup(product: str, client_call: str, client: LinodeClient, storage: str,
           s3_id: str, s3_secret: str, s3_url: str) -> None:
    """Backup objects"""
    objects = eval(f"client.{client_call}()")
    if storage.startswith("s3://"):
        bucket = storage[5:]
        linode_obj_config = {
            "aws_access_key_id": s3_id,
            "aws_secret_access_key": s3_secret,
            "endpoint_url": s3_url,
        }
        client = boto3.client("s3", **linode_obj_config)
        for object in objects:
            date = object.updated.strftime("%Y%m%d%H%M%S")
            file_name = f"{object.id}+{date}"
            full_file_name = f"{product}/{file_name}.json"
            try:
                client.head_object(Bucket=bucket, key=full_file_name)
            except:
                file_content = json.dumps(object._raw_json)
                client.put_object(Body=file_content, Bucket=bucket, Key=full_file_name)
    else:
        if not os.path.exists(product):
            os.makedirs(f"{storage}/{product}")
        for object in objects:
            date = object.updated.strftime("%Y%m%d%H%M%S")
            file_name = f"{object.id}+{date}"
            full_file_name = f"{storage}/{product}/{file_name}.json"
            if not os.path.exists(full_file_name):
                with open(full_file_name, "w") as file:
                    json.dump(object._raw_json, file)
