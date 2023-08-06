=================
The Plumb Library
=================

:Author:   Spectro
:Date:     2018-10-01
:Version:  $Revision: 1.2.5 $
:License:  MIT License

Provides higher level interfaces to work with data producers and consumers. ``plumb`` supports five backends: RabbitMQ,
Redis, Amazon SQS and SNS services, Kafka, and a memory implementation (designed to be a testing artifact).

The focus is on **python 3** and **boto3** (for AWS support).

-------
The API
-------

``plumb`` uses the concepts of *Source* and *Sink* to abstract the backend. Data is transfered encoded in JSON, and by
default compressed using zlib.

To fetch raw packages use a "Package Source" object, which handles a backend connection and its configuration and
exposes a "get()" method. Similarly, a "Package Sink" object exposes a "put(pkg)" method.

You can either create the Sources and Sinks directly by instantiating them from their packages or use the convenience
factory functions exposed in the ``plumb`` package. This functions receive a JSON with the configuration for the Sources
or Sinks and returns a list of such configured devices.

-----
Tests
-----

The library is provided with unit tests and integration tests for Redis and AWS. To run the unit tests::

  python setup.py test

or using ``nose``::

  nosetests tests/unit

The integration tests can be run using nose::

  nosetests tests/integration

**Keep in mind** that ``boto3`` will fetch your AWS credentials. It currently tries the environment variables ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``, then tries the ``~/.aws`` directory. For details, see `Boto3 Credentials Configuration <http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials>`__.
