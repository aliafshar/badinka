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

"""Tiny wrapper to generate the BaDinka reference docs"""

import os
import sys
import dataclasses

import jinja2
import pdoc


@dataclasses.dataclass
class Example:
  name: str
  summary: str
  description: str
  source: str
  
  @property
  def filename(self):
    return f'{self.name}.py'

  @property
  def path(self):
    return f'examples/{self.filename}'

  @classmethod
  def from_mod(cls, mod):
    doclines = mod.docstring.splitlines()
    summary = doclines[0]
    description = '\n'.join(doclines[1:]).strip()
    srclines = mod.source.splitlines()[15 + len(doclines):-1]
    source = '\n'.join(srclines).strip().replace('\n\n\n', '\n\n')
    return cls(
        name = mod.name,
        summary = summary,
        description = description,
        source = source,
    )


def write_module(name, html):
  path = f'docs/public/{name}.html'
  print(f'{name} -> {path}')
  with open(path, 'w') as f:
    f.write(html)

def write_reference_docs():
  context = pdoc.Context()
  mod = pdoc.Module('badinka', context=context)
  write_module('index', mod.html())

def write_readme():
  f = open('docs/README.jinja2.md')
  t = jinja2.Template(f.read())
  f.close()
  config_instruction, config_source = read_config()
  out = t.render(
      subtitle = read_docstring(),
      examples = read_examples(),
      motivation = read_motivation(),
      config_instruction = config_instruction,
      config = config_source,
      options = read_options(),
  )
  f = open('README.md', 'w')
  f.write(out)
  f.close()


def read_config():
  context = pdoc.Context()
  mod = pdoc.Module('badinka._config', context=context)
  cls = mod.classes()[0]
  srclines = cls.source.splitlines()
  alines = []
  for l in srclines:
    if l.strip().startswith('def'):
      break
    alines.append(l)
  csource = '\n'.join(alines)
  ilines = mod.docstring.splitlines()[1:]
  isource = '\n'.join(ilines)
  return isource, csource


def read_options():
  context = pdoc.Context()
  mod = pdoc.Module('badinka._generation', context=context)
  for cls in mod.classes():
    if cls.name == 'Options':
      break
  srclines = cls.source.splitlines()
  alines = []
  for l in srclines:
    if l.strip().startswith('def'):
      break
    alines.append(l)
  csource = '\n'.join(alines)
  return csource


def read_motivation():
  f = open('docs/motivation.md')
  howto = f.read()
  f.close()
  return howto


def read_docstring():
  context = pdoc.Context()
  mod = pdoc.Module('badinka', context=context)
  return mod.docstring


def read_examples():
  eg_names = [
      'gen0',
      'gen1',
      'gen2',
      'gen3',
      'gen4',
      'rag0',
      'chain0',
      'tool0',
      'rag2',
      'rag1',
  ]
  sys.path.append('examples')
  context = pdoc.Context()
  egs = []
  for eg_name in eg_names:
    mod = pdoc.Module(eg_name, context=context)
    print(mod.name, mod.qualname)
    egs.append(Example.from_mod(mod))
  return egs


def main():
  write_reference_docs()
  write_readme()
  

if __name__ == '__main__':
  main()

# vim: ft=python sw=2 ts=2 sts=2 tw=120
