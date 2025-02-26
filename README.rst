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

.. code-block:: python

   pipx install yesterdaypy

| If you need Linode Object Storage to store the backup, install Boto3.

.. code-block:: python

   pipx inject yesterdaypy boto3

| You can also clone this repository and run:

.. code-block:: python

   python yesterdaypy/yesterdaypy.py

How to use it?
--------------
| First, you need to setup the necessary environment variables.
|
| Linode token is mandatory:

.. code-block:: python

   export LINODE_TOKEN=ABC

| If using Linode Object Storage:

.. code-block:: python

   export AWS_ACCESS_KEY_ID=ABC
   export AWS_SECRET_ACCESS_KEY=ABC
   export AWS_ENDPOINT_URL=ABC

| Run the software:

.. code-block:: python

   yesterdaypy

| It will backup all objects to the current directory, for all supported products, with a folder per product.

| To backup to a specific folder, specify the location.

.. code-block:: python

   yesterdaypy --storage /home/user/backup/example/

| To backup to Linode Object Storage, storage needs to start with **s3://** followed by the bucket name.

.. code-block:: python

   yesterdaypy --storage s3://bucket-name

| You can also use **--products** to limit the products you want to backup.
| Use **--errors** to get the list of errors.
| Lastly, **--help** for the help information.

To do
-----
* Debug
    Add debug options for troubleshooting.
* Verbose
    Add verbosity to make visible what the software is doing.
* Products
    Add more products.
* Thread
    Add threads for large configurations.

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
