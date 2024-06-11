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


import pytest
import badinka

_options = badinka.Options(tokens=16)
_config = badinka.Config(generation_model='orca-mini')

def test_docs():
  p = badinka.Conductor()
  assert 'default' == p.docs.collection().name

@pytest.mark.skipif("not config.getoption('integration')")
def test_generate_from_prompt():
  p = badinka.Prompt(template='why is the sky {{q}}?')
  badinka.Conductor().generate(p, options=_options, q='blue')

# vim: ft=python sw=2 ts=2 sts=2 tw=120
