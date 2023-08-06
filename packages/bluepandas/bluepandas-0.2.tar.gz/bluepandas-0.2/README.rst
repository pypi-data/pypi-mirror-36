===========
BluePandas |badge|_
===========

A Python library to read files in Azure Blob Storage as Pandas DataFrames

Installation
-------------

The latest version is available on PyPI::

    pip install bluepandas

Example
--------

The library reads an environment variable containing the connection string to your
blob storage account. The variable must be named ``AZ_<STORAGE-ACCOUNT-NAME>``  
and set to your connection string, which is obtained from the Azure Portal by 
navigating to you storage account under settings/access keys as shown below


.. image:: http://i67.tinypic.com/25sljxt.png

Short example on usage::

    import bluepandas

    df = bluepandas.read_csv("wasbs://<container-name>@<storage-account-name>.blob.core.windows.net/path/to/your.csv")


.. |badge| image:: https://dev.azure.com/nihil0/bluepandas/_apis/build/status/nihil0.bluepandas
.. _badge: https://dev.azure.com/nihil0/bluepandas/_build/latest?definitionId=1


