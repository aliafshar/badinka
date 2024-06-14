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

"""External Tools support"""

import json
from dataclasses import dataclass, field

from ._parsing import Parser

class Tool:

  name: str
  description: str
  arguments: dict[str, any]

  def do(self, **kw):
    raise NotImplementedError

  def as_dict(self):
    return {
        'name': self.name,
        'description': self.description,
        'arguments': self.arguments,
    }

class ToolParser(Parser):

  def __init__(self, tool):
    self.tool = tool
    self.parameters = {}

  def match(self, reply):
    return reply.content.startswith(f':T:{self.tool.name}:')

  def parse(self, reply):
    reply.parser = self
    reply.tool = self.tool
    parts = reply.content.split(':')
    kw = json.loads(':'.join(parts[3:]))
    if 'arguments' in kw:
      kw = kw['arguments']
    self.parameters = kw
    return self.tool.do(**kw)


# vim: ft=python sw=2 ts=2 sts=2 tw=80
