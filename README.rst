What is YesterdayPy? - TLDR Version
-----------------------------------
| A Python software to backup Linode configuration to local folder or Linode Object Storage.

What is YesterdayPy? - Longer Version
-------------------------------------
| Have you asked the question "How was this configured yesterday?" while working with Linode, or any of the variations with the same meaning?
| If yes, YesterdayPy will help you find the answer.
| If no, well, you are in the wrong corner of the Internet.
|
| Note: There was already a project called yesterday in PyPI, so I just added Py in front of the name.
|
| YesterdayPy creates a backup of your configuration in Linode.
| For each Linode product (Firewall for example), the software will create a JSON file for each object you created.
| The file will be named using format ID+date.json, with ID being the ID of the object (every Linode object has an ID), and date is the last update date.
| If the file already exists, no file is created. That means, it only backup the changes since last backup.
|
| If you want to know how the object was configured yesterday while troubleshooting a problem, you can just compare the current version with the JSON file.

Technical Bits
--------------
| Requires Python version 3.9 or above.
| Requires linode_api4 (https://github.com/linode/linode_api4-python)
| If using to backup configuration to Linode Object Storage, Boto3 is also required (https://github.com/boto/boto3)

Installation
------------
| Use pipx (https://github.com/pypa/pipx) to install YesterdayPy.

.. code-block:: python

   pipx install yesterdaypy

| If you need Linode Object Storage, install Boto3.

.. code-block:: python

   pipx inject yesterdaypy boto3

sss
