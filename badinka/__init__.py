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

"""Minimalist AI orchestration library for local LLMs

## Hello World

The simplest and least useful example:

```python
import badinka

c = badinka.Conductor()
c.generate('why is the sky blue?')
```

## Retrieval Augmented Generation

This example performs a similarity search on the query for the top 10 documents
in the database and injects them into the context of the instruction and
replies as a scientist would.

```python
import badinka as bd

c = bd.Conductor()
c.docs.add(bd.Document(content='the sky is blue because of fairies'))
reply = c.generate(
  instruction = Instruction(
    role = 'scientist',
    prompt = 'why is the sky blue?',
    inject = Injection(),
  ),
)
print(reply.content)
```
```markdown
The sky appears blue due to a phenomenon known as **Rayleigh scattering**. 

When sunlight interacts with molecules in the atmosphere, two
key processes influence the color we perceive:

**1. Scattering:**

- Sunlight is composed of various wavelengths...<snip>
```
"""

__version__ = '0.1'


from ._conductor import Conductor
from ._config import Config
from ._documents import Document, DocumentStore, Query
from ._generation import Generator, Prompt, Reply, Instruction, \
    Options, Injection


__all__ = [
    'Conductor',
    'Config',
    'Document',
    'DocumentStore',
    'Generator',
    'Instruction',
    'Prompt',
    'Query',
    'Reply',
]


# vim: ft=python sw=2 ts=2 sts=2 tw=80
