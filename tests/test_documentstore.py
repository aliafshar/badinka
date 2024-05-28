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



import badinka as bd


def test_add_document_default():
  d = bd.Document(content='I am a doc')
  ds = bd.DocumentStore(bd.Config())
  ds.append(d)
  r = bd.DocumentList.from_get_response(
      ds.collection().peek(1))
  assert d.id == r[0].id

def test_document_auto_id():
  d = bd.Document(content='I am a doc')
  assert 'I am a doc' == d.content
  assert d.id

def test_document_passed_id():
  d = bd.Document(content='I am a doc', id='123')
  assert 'I am a doc' == d.content
  assert '123' == d.id

def test_collections():
  ds = bd.DocumentStore(bd.Config())
  c1 = ds.collection('banana')
  assert 'banana' == c1.name
  c2 = ds.collection('banana')
  assert 'banana' == c2.name

def test_documentlist():
  ds = bd.DocumentList()
  doc = bd.Document(content='hello')
  ds.documents.append(doc)
  assert len(ds) == 1
  assert list(ds) == [doc]
  assert doc in ds


# vim: ft=python sw=2 ts=2 sts=2 tw=120
