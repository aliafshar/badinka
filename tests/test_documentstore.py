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



import badinka


def test_add_document_default():
  d = badinka.Document(content='I am a doc')
  ds = badinka.DocumentStore(badinka.Config())
  ds.append(d)
  r = ds.collection().peek(1)
  ds.config.log.debug(ds.documentify(r))
  assert d.id == r['ids'][0]

def test_document_auto_id():
  d = badinka.Document(content='I am a doc')
  assert 'I am a doc' == d.content
  assert d.id

def test_document_passed_id():
  d = badinka.Document(content='I am a doc', id='123')
  assert 'I am a doc' == d.content
  assert '123' == d.id

def test_collections():
  ds = badinka.DocumentStore(badinka.Config())
  c1 = ds.collection('banana')
  assert 'banana' == c1.name
  c2 = ds.collection('banana')
  assert 'banana' == c2.name


# vim: ft=python sw=2 ts=2 sts=2 tw=120
