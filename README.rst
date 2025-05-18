What is YesterdayPy? - TLDR Version
-----------------------------------
| A Python software to backup Linode configuration to a local folder or Linode Object Storage.

What is YesterdayPy? - Longer Version
-------------------------------------
| Have you asked the question "How was this configured yesterday?" while working with Linode, or any of the variations with the same meaning?
| If yes, YesterdayPy will help you find the answer.
| If no, well, you are in the wrong corner of the Internet.
|
| Note: A project called yesterday was already in PyPI, so I just added Py in front of the name.
|
| YesterdayPy creates a backup of your Linode configuration.
| For each Linode product (Firewall for example), the software will create a JSON file for each object you have.
| The file will be named using the format **ID+date.json**, with ID being the object's ID (every Linode object has an ID), and date being the last update date.
| If the file already exists, no file is created. That means, it will only backup the changes since the last backup.
|
| If you want to know how the object was configured yesterday while troubleshooting a problem, you can then just compare the current version with the JSON file.

Technical Bits
--------------
| Requires Python version 3.9 or above.
| Requires **linode_api4** (https://github.com/linode/linode_api4-python).
| If used to backup configuration to Linode Object Storage, **Boto3** is also required (https://github.com/boto/boto3).
| Currently supports the following products Firewall, Linode, LKE, and VPC.

Installation
------------
| Use pipx (https://github.com/pypa/pipx) to install YesterdayPy.

.. code-block:: bash

   pipx install yesterdaypy

| If you need Linode Object Storage to store the backup, install Boto3.

.. code-block:: bash

   pipx inject yesterdaypy boto3

| You can also clone this repository and run:

.. code-block:: bash

   python yesterdaypy/yesterdaypy.py

How to use it?
--------------
| First, you need to setup the necessary environment variables.
|
| Linode token is mandatory:

.. code-block:: bash

   export LINODE_TOKEN=ABC

| If using Linode Object Storage:

.. code-block:: bash

   export AWS_ACCESS_KEY_ID=ABC
   export AWS_SECRET_ACCESS_KEY=ABC
   export AWS_ENDPOINT_URL=ABC

| Run the software:

.. code-block:: bash

   yesterdaypy

| It will backup all objects to the current directory, for all supported products, with a folder per product.

| To backup to a specific folder, specify the location.

.. code-block:: bash

   yesterdaypy --storage /home/user/backup/example/

| To backup to Linode Object Storage, storage needs to start with **s3://** followed by the bucket name.

.. code-block:: bash

   yesterdaypy --storage s3://bucket-name

| You can also use **--products** to limit the products you want to backup.
| Use **--errors** to get the list of errors.
| Use **--output** to print basic information.
| Use **--verbose** to print extra information.
| Use **--debug** to print debug information.
| Lastly, **--help** for the help information.

Docker
------
| You can use the Dockerfile in this repository to build a local image.
| Also, the image is available from DockerHub.
|
| Use the export command to setup the necessary environment variables.
| Example using DockerHub:

.. code-block:: bash

   docker run -e LINODE_TOKEN \
   --mount type=bind,src=.,dst=/usr/local/yesterdaypy \
   leonardobdes/yesterdaypy:latest

| This will save the files to the current folder.
| You don't need the mount option to save to Linode Object Storage.

Systemd Service
---------------
| The most common setup will be to run YesterdayPy daily.
| You can do that using a systemd service and timer.
| Copy the files **yesterdaypy.service** and **yesterdaypy.timer** to the folder **/etc/systemd/system/**.
|
| The timer is configured to run daily at midnight, so change it based on your preference.
| The service has 2 examples, the first command runs the software after installation using pipx, and the second one using Docker.
| In both cases, it read the Linode token from the file **linode_token.txt**.

jq
--
| Download from https://github.com/jqlang/jq
| Use jq to print the text formatted.
| You can also use the online version https://play.jqlang.org/

.. code-block:: bash

  $ jq . 1056933+20250222233724.json
  {
    "id": 1056933,
    "label": "test-fw",
    "created": "2024-10-22T22:38:26",
    "updated": "2025-02-22T23:37:24",
    "status": "enabled",
    "rules": {
      "inbound": [
        {
          "action": "ACCEPT",
          "addresses": {
            "ipv4": [
              "1.1.1.1/32"
            ]
          },
          "ports": "22",
          "protocol": "TCP",
          "label": "test-ssh",
          "description": null
        }
      ],
      "inbound_policy": "DROP",
      "outbound": [],
      "outbound_policy": "ACCEPT",
      "version": 3,
      "fingerprint": "cb6bf75b"
    },
    "tags": [],
    "entities": [
      {
        "id": 72473810,
        "type": "linode",
        "label": "ubuntu-gb-lon",
        "url": "/v4/linode/instances/72473810"
      }
    ]
  }

| You can query a specific part.

.. code-block:: bash

  $ jq .rules.inbound 1056933+20250222233724.json
  [
    {
      "action": "ACCEPT",
      "addresses": {
        "ipv4": [
          "1.1.1.1/32"
        ]
      },
      "ports": "22",
      "protocol": "TCP",
      "label": "test-ssh",
      "description": null
    }
  ]

jd
--
| Download from https://github.com/josephburnett/jd
| Use jd to compare 2 JSON files.
| You can also use the online version http://play.jd-tool.io/

.. code-block:: bash

  $ jd 1056933+20250222233724.json 1056933+20250314231035.json
  @ ["entities",0]
  [
  - {"id":72473810,"label":"ubuntu-gb-lon","type":"linode","url":"/v4/linode/instances/72473810"}
  ]
  @ ["rules","fingerprint"]
  - "cb6bf75b"
  + "69cc1741"
  @ ["rules","inbound",1]
    {"action":"ACCEPT","addresses":{"ipv4":["1.1.1.1/32"]},"description":null,"label":"test-ssh","ports":"22","protocol":"TCP"}
  + {"action":"ACCEPT","addresses":{"ipv4":["0.0.0.0/0"],"ipv6":["::/0"]},"description":null,"label":"icmp","protocol":"ICMP"}
  ]
  @ ["rules","version"]
  - 3
  + 4
  @ ["updated"]
  - "2025-02-22T23:37:24"
  + "2025-03-14T23:10:35"

To do
-----
* Products
    Add more products.
    Also, some objects have other obejcts under it (Linode Configuration Profile).
* Thread
    Add threads for large configurations.
* Mac OS
    Test on MacOS, it should work.
* Windows
    Need some changes to work on Windows.

Other software ideas
--------------------
* YesterdayPy_Clone
    Clone an object with a new label (name).
* YesterdayPy_Restore
    Restore the object to the configuration of the JSON file.

Author
------

| Name:
| Leonardo Souza
| LinkedIn:
| https://uk.linkedin.com/in/leonardobdes

How to report bugs?
-------------------

| Use `GitHub <https://github.com/leonardobdes/yesterdaypy/issues>`_ issues to report bugs.

How to request new functionalities?
-----------------------------------

| Use `GitHub <https://github.com/leonardobdes/yesterdaypy/issues>`_ issues to request new functionalities.
| Use the following format in the title **RFE - Title**.
