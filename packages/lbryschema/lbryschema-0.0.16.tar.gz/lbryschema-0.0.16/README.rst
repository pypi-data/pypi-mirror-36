==============================
lbryschema |travis| |coverage|
==============================

.. _introduction:

lbryschema is a `protobuf <https://github.com/google/protobuf>`_ schema that defines how claims are structured and validated in the LBRY blockchain.
There is also code to construct, parse, and validate lbry:// URIs.


Installation
============

To install lbryumschema, run the following command (use of a virtualenv is recommended):

.. code-block:: shell

    pip install git+https://github.com/lbryio/lbryschema.git


Usage
=====

See `resources/schema.md <https://github.com/lbryio/lbry.tech/tree/master/documents/resources/schema.md>`_ in the lbry.tech repo.


Development
===========

To install in development mode, check out this repository and inside it run:

.. code-block:: shell

    pip install -r requirements.txt
    pip install -e .


To run the tests:

.. code-block:: shell

    cd tests/
    python -m unittest discover -v


To re-compile the protobuf files (only necessary if you've changed any of the ``.proto`` files) you must first install the ``protoc`` tool.

On macOS this is done with ``brew`` command:

.. code-block:: shell

    brew install protobuf


On Ubuntu you can install everything with ``apt-get``:

.. code-block:: shell

    sudo apt-get install protobuf-compiler python-protobuf
 

Once protobuf is installed, run ``./build.sh`` script to compile the .proto files.


.. |travis| image:: https://travis-ci.org/lbryio/lbryschema.svg?branch=master
   :target: https://travis-ci.org/lbryio/lbryschema
   :alt: Build

.. |coverage| image:: https://codecov.io/gh/lbryio/lbryschema/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/lbryio/lbryschema
   :alt: Test Coverage
