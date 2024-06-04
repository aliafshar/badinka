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

"""Geography tutor

This example fetches, parses and loads an open Human Geography textbook, and
uses it to ground responses about this topic.

### Query

> Why to people migrate?

### Rendered prompt

> You should behave as a teacher.
> Using only the following context, answer the question below:
> 
> Context: As people migrate or move to anew area, they bring their ideas,
> objects, and the like with them in a process call
> Most migrants move for better jobs, higher incomes, and better opportunities
> overall
> People move and they mix with other groups of people
> Even though people generally migrate to find/make a better life for themselves
> and for their families, the benefits and pitfalls of migration affect
> different countries and regions in very different ways
> Rural residents are more migratory than those in towns
> While geographers try to understand where people move and why, a more
> significant question might be why so many people move
> Regardless of the time period, modern humans have been on the move for a very
> long time—a trend that has accelerated in recent years owing to cheap
> transportation and easier access to information by potential migrants
> Different people can have different adaptations to similar places
> 
> why do people migrate?

### Output (e.g.)

> People migrate for better jobs, higher incomes, and better opportunities
> overall.
"""

# https://oer.galileo.usg.edu/geo-textbooks/2/
original_url = ('https://oer.galileo.usg.edu/cgi/viewcontent.cgi?'
                'article=1002&context=geo-textbooks')

import PyPDF2

import badinka as bd

config = bd.Config(
    vector_store_path = 'examples/data/geography.chroma'
)

def fetch():
  import urllib.request 
  urllib.request.urlretrieve(original_url, 'examples/data/geography.pdf')

def extract():
  reader = PyPDF2.PdfReader('examples/data/geography.pdf')
  lines = []
  def _visit(text, cm, tm, font, size, lines=lines):
    if font and font['/BaseFont'] == '/PFELHC+Georgia' and tm[0] == 11.0:
      if t := text.rstrip('\n'):
        if '/Widths' in font:
          del font['/Widths']
        lines.append(t)
  for page in reader.pages[9:]:
    page.extract_text(visitor_text=_visit)
  f = open('examples/data/geography.txt', 'w')
  f.write(''.join(lines))
  f.close()


def embed():
  conductor = bd.Conductor(config)
  f = open('examples/data/geography.txt')
  raw = f.read()
  sentences = raw.split('.')
  for i, s in enumerate(sentences):
    print(f'{i+1} of {len(sentences)}')
    if t := s.strip():
      conductor.docs.append(bd.Document(content=t))


def query(q):
  conductor = bd.Conductor(config)
  reply = conductor.generate(
    bd.Instruction(
        role = 'a teacher',
        prompt = bd.Prompt(q),
        inject = bd.Injection(
          n_results=30,
        ),
    ),
    options = bd.Options(
        output_tokens = 32,
    ),
  )
  print(reply.content)
  


if __name__ == '__main__':
  #embed()
  query('why do people migrate?')


# vim: ft=python sw=2 ts=2 sts=2 tw=80
