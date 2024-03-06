# ArangoDBDocumentStore

> Showcasing a possible implementation of the ArangoDB Document Store protocol
> for [Haystack 2.x](https://docs.haystack.deepset.ai/v2.0) in Python.


This Python module provides an implementation of the `DocumentStore` protocol for ArangoDB, allowing you to read, write,
and delete documents from an ArangoDB collection.

## Overview

The `ArangoDBDocumentStore` class serves as a wrapper around the `arango` package, which provides a Python client for
ArangoDB. It implements the `DocumentStore` protocol methods to interact with documents stored in an ArangoDB
collection.

## Installation

To use this module, you need to have the following dependencies installed:

- `arango` (Python client for ArangoDB)
- `haystack` (Python library for building transformer models and other NLP components)
- `pandas` (for data manipulation and analysis)

You can install these dependencies using `pip`:

```shell
pip install --upgrade -r requirements.txt
```

or if you have [Taskfile](https://taskfile.dev/) installed:

```shell
task install
```

## Usage

**Configure the ArangoDBDocumentStore**

First, you need to configure the `ArangoDBDocumentStore` with the necessary connection details:

```python
from store import ArangoDBDocumentStoreConfig, ArangoDBDocumentStore

config = ArangoDBDocumentStoreConfig(
    connection_url="http://localhost:8529",
    database_name="my_database",
    username="my_username",
    password="my_password",
    collection_name="my_collection"
)

document_store = ArangoDBDocumentStore(config)
```

**Write Documents**

You can write documents to the ArangoDB collection using the `write_documents` method:

```python
from haystack import Document

documents = [
    Document(content="This is the first document."),
    Document(content="This is the second document.", meta={"category": "example"})
]

document_store.write_documents(documents)
```

**Get Document by ID**
Retrieve a document by its ID using the get_document method:

```python
document = document_store.get_document("document_id")
```

**Update Documents**

Update existing documents in the ArangoDB collection using the update_documents method:

```python
import time

last_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

updated_documents = [
    Document(content="This is the updated first document.", meta={"lastUpdated": last_updated}),
    Document(content="This is the updated second document.", meta={"lastUpdated": last_updated})
]

num_updated = document_store.update_documents(updated_documents)
```

**Delete Documents**

Delete documents from the ArangoDB collection by providing their IDs using the delete_documents method:

```python
document_ids_to_delete = ["document_id_1", "document_id_2"]
document_store.delete_documents(document_ids_to_delete)
```

**Filter Documents**

Retrieve documents that match specific filters using the filter_documents method:

```python
filters = {"category": "example"}
filtered_documents = document_store.filter_documents(filters)
```

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the
project's repository.