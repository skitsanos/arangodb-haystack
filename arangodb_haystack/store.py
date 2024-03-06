"""
This module contains an implementation of the `DocumentStore` protocol for ArangoDB.
The `ArangoDBDocumentStore` class is a wrapper around the `arango` package, which provides a Python
client for ArangoDB. The `ArangoDBDocumentStore` class implements the `DocumentStore` protocol
methods to read, write, and delete documents from an ArangoDB collection.
"""
from dataclasses import dataclass
from typing import List, Dict, Protocol, Any, Optional

from arango import ArangoClient
from haystack import Document
from pandas import DataFrame


@dataclass
class ArangoDBDocumentStoreConfig:
    """
    Configuration for an ArangoDBDocumentStore.
    """
    connection_url: str
    database_name: str
    username: str
    password: str
    collection_name: str
    verify: bool = False


class ArangoDBDocumentStore(Protocol):
    """
    A protocol for a document store that can read, write, and delete documents.
    """

    def __init__(self, config: ArangoDBDocumentStoreConfig):
        self.client = ArangoClient(hosts=config.connection_url)

        self.db = self.client.db(config.database_name,
                                 config.username,
                                 config.password,
                                 verify=config.verify)

        self.collection = self.db.collection(config.collection_name)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes this store to a dictionary.
        """
        return {
            "type": "ArangoDBDocumentStore",
            "connection_url": self.client.hosts,
            "database_name": self.db.name,
            "collection_name": self.collection.name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArangoDBDocumentStore":
        """
        Deserializes the store from a dictionary.
        """
        return cls(**data)

    def count_documents(self) -> int:
        """
        Returns the number of documents stored.
        """
        return self.collection.count()

    def write_documents(self, documents: list[Document]):
        """
        Writes documents into the Document Store.
        :param documents:
        :return:
        """
        for doc in documents:
            # Convert a Haystack document to ArangoDB document format (e.g., dictionary)
            arango_doc = convert_to_arango_doc(doc)
            self.collection.insert(arango_doc)

    def get_document(self, document_id: str) -> Document:
        """
        Get a document by its ID.
        """
        arango_doc = self.collection.get(document_id)
        return convert_from_arango_doc(arango_doc)

    def update_documents(self, documents: List[Document]) -> int:
        """
        Writes (or overwrites) documents into the DocumentStore, return the number of documents
        that were written.

        Args:
            documents: List of Haystack documents to update.

        Returns:
            Number of documents that were written.
        """

        updated_count = 0
        for doc in documents:
            arango_doc = convert_to_arango_doc(doc)
            arango_id = doc.meta.get("id")  # Assuming Haystack document has an 'id' field in meta

            if not arango_id:
                # Handle the case where a Haystack document doesn't have an ID for update
                # ... (implement logic based on policy)
                pass
            else:
                # Update an existing document based on Haystack document ID (arango_id)
                update_result = self.collection.update(
                    document=arango_doc, check_rev=True, merge=True, keep_none=True
                )
                if len(update_result.items()) == 0:
                    # Handle potential update errors (e.g., logging or raising exceptions)
                    pass
                else:
                    updated_count += 1

        return updated_count

    def delete_documents(self, document_ids: List[str], ignore_missing=True) -> None:
        """
        Deletes all documents with matching document_ids from the Document Store.
        """
        for document_id_to_delete in document_ids:
            self.collection.delete(document_id_to_delete, ignore_missing=ignore_missing)

    def filter_documents(self, filters: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Return the documents that match the provided filters.

        Args:
            filters: Optional dictionary specifying filters for document retrieval.

        Returns:
            List of Haystack Document objects matching the filters.
        """

        if not filters:
            # No filters provided, return all documents
            cursor = self.collection.find({})
        else:
            # Build AQL filter query string based on provided filters
            filter_query = build_filter_query(filters)
            cursor = self.db.aql.execute(f"FOR doc IN {self.collection.name} "
                                         f"FILTER {filter_query} RETURN doc")

        return [convert_from_arango_doc(doc) for doc in cursor]


def convert_to_arango_doc(doc: Document) -> Dict[str, Any]:
    """
    Converts Haystack Document to ArangoDB document format.

    Args:
        doc: Haystack Document object.

    Returns:
        Dictionary representing the ArangoDB document.
    """

    arango_doc: dict[str, str | DataFrame | dict[str, Any] | Any] = {
        "content": doc.content,
        "meta": doc.meta.copy(),  # Create a copy to avoid modifying an original Haystack document
    }

    # Handle potential 'id' field in Haystack document meta
    haystack_id = arango_doc["meta"].get("id")

    if haystack_id:
        del arango_doc["meta"]["id"]  # Remove 'id' from meta to avoid conflicts

    # Set ArangoDB _id attribute if a Haystack document has an 'id'
    arango_doc["_id"] = haystack_id

    # ... (Add additional fields to arango_doc as needed)

    return arango_doc


def convert_from_arango_doc(doc: Dict[str, Any]) -> Document:
    """
    Converts ArangoDB document to Haystack Document format.
    :param doc:
    :return:
    """
    meta = doc.get("meta", {})
    meta = {**meta, "id": doc["_id"]}  # Combine dictionaries using spread operator
    return Document(
        content=str(doc.get("content", None)),
        meta=meta,
    )


def build_filter_query(filters: Dict[str, Any]) -> str:
    """
    Builds an AQL filter query string based on the provided filters' dictionary.

    Args:
        filters: Dictionary specifying filters for document retrieval.

    Returns:
        A string representing the AQL filter query.
    """

    filter_parts = []
    for field, value in filters.items():
        # Implement logic to translate filter field and value to AQL syntax
        # Consider different filter types (e.g., equality, range, etc.)
        filter_parts.append(f"LIKE(doc.{field}, '%%{value}%%', true)")  # Example equality filter

    return " AND ".join(filter_parts) if filter_parts else "true"  # Combine filter parts with AND
