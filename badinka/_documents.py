# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Documentation storage in Chroma vectors"""

from loguru import logger as log

from dataclasses import dataclass, field
from collections import abc
from uuid import uuid4

from chromadb import Collection
from chromadb import EphemeralClient, PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction


from ._config import Config



@dataclass
class Document:
  """Document is the unit of storage in the vector database.
  
  It must contain some content, and all other fields are optional. If an ID is
  not supplied, one is automatically generated.
  """

  #: The text content of the document.
  content: str
  
  #: The ID of the document. All documents stored in the vector database need an
  #: ID, and this is automatically generated ising `uuid.uuid4` if not provided.
  id: str = field(default_factory=lambda: str(uuid4()))

  #: An arbitrary set of key, values stored for later retrieval. This can be
  #: extremely useful for:
  #: 
  #: 1. storing data
  #: 2. adding parameters for querying against
  meta: dict[str, any] = None

  #: The generated embeddings for the document. These are currently only for
  #: reading as they are generated on document storage, but could be used to
  #: store if they are provided.
  embeddings: list[float] = field(default=None, repr=False)


class DocumentList(abc.Sequence):
  """List of documents from querying the document store."""

  def __init__(self):
    self.documents: list[Document] = []

  def __getitem__(self, index) -> Document:
    return self.documents[index]

  def __len__(self) -> int:
    return len(self.documents)

  @classmethod
  def from_query_response(cls,
      response) -> abc.Sequence[Document]:
    """Parse a chromadb response for a query."""
    return cls.from_response(
        ids = response['ids'][0],
        contents = response['documents'][0],
        embeddings = response['embeddings'][0],
        metadatas = response['metadatas'][0],
    )

  @classmethod
  def from_get_response(cls,
      response) -> abc.Sequence[Document]:
    """Parse a chromadb response for a get."""
    return cls.from_response(
        ids = response['ids'],
        contents = response['documents'],
        embeddings = response['embeddings'],
        metadatas = response['metadatas'],
    )

  @classmethod
  def from_response(cls,
      ids: list[str],
      contents: list[str],
      embeddings: list[float],
      metadatas: list[dict[str, any]]
  ) -> abc.Sequence[Document]:
    """Parse a chromadb response."""
    ds = cls()
    for i, id in enumerate(ids):
      d = Document(content=contents[i], id=id)
      if metadatas:
        d.metadata = metadatas[i]
      if embeddings:
        d.embeddings = embeddings[i]
      ds.documents.append(d)
    return ds


@dataclass
class Query:
  """Contains the information required to query the database.
  """
  #: A text query. Since the underlying API offers a list of text queries, this
  #: is a convenience to save wrapping every text in a list.
  text: str = None

  #: A list of text queries. If provided along with the `text` attribute, the
  #: two are combined.
  texts: list[str] = field(default_factory=list)

  # An embedding to query similarity for.
  embeddings: list[float] = field(default_factory=list)

  # The number of results to return.
  n_results: int = 10

  def as_args(self) -> dict[str, any]:
    """Converts the stored attributes into chroma query keyword arguments."""
    texts = list(self.texts)
    if self.text:
      texts.insert(0, self.text)
    return {
        'query_texts': texts,
        'include': ['documents', 'metadatas', 'embeddings', 'distances'],
        'n_results': self.n_results,
    }


class DocumentStore:
  """Stores and retrieves documents in a vector database

  In our case, we use ChromaDB.
  """

  def __init__(self, config: Config):
    self.config = config
    self.embedding_function = OllamaEmbeddingFunction(
        url=self.config.embeddings_url,
        model_name=self.config.embeddings_model_name,
    )

  def client(self):
    """Create a chromadb client."""
    if self.config.vector_store_path == ':memory:':
      return EphemeralClient()
    else:
      return PersistentClient(self.config.vector_store_path)

  def collection(self, collection_name: str = 'default') -> Collection:
    """Get or create an existing or the default collection."""
    return self.client().get_or_create_collection(
        collection_name,
        embedding_function=self.embedding_function,
    )

  def append(self, doc, collection_name='default'):
    """Add a single document to the named collection or default."""
    self.extend([doc], collection_name=collection_name)

  def extend(self, docs, collection_name='default') -> None:
    """Add multiple documents to the named collection or default."""
    c = self.collection(collection_name=collection_name)
    c.add(
      ids=[d.id for d in docs],
      metadatas=[d.meta for d in docs],
      documents=[d.content for d in docs])

  def query_text(self, text, n_results=10,
      collection_name='default') -> list[Document]:
    """Query the documents for a single text query."""
    q = Query(
        texts = [text],
        n_results = n_results,
    )
    return self.query(q, collection_name=collection_name)

  def query(self, query: Query,
      collection_name='default') -> list[Document]:
    """Query the documents."""
    c = self.collection(collection_name=collection_name)
    results = c.query(**query.as_args())
    return DocumentList.from_query_response(results)

  def all(self, collection_name='default'):
    c = self.collection(collection_name=collection_name)
    return DocumentList.from_get_response(c.peek(c.count()))

  def __len__(self):
    c = self.collection(collection_name='default')
    return c.count()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
