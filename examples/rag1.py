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
> `<snipped>`
>
> why do people migrate?

### Output (e.g.)

> **Factors influencing human migration:**
> 
> **Economic factors:**
> 
> * Lack of job opportunities
> * Low wages
> * Economic instability
> * High cost of living
> 
> 
> **Socio-cultural factors:**
> 
> * Cultural differences
> * Social networks
> * Family reunification
> * Desire for better education
> 
> 
> **Political factors:**
> 
> * Political persecution
> * War and conflict
> * Seeking asylum
> * Political instability
> 
> 
> **Environmental factors:**
> 
> * Climate change
> * Natural disasters
> * Environmental degradation
> 
> 
> **General relationship between demographic factors and migration across time:**
> 
> * Population growth and urbanization
> * Economic development and inequality
> * Political and social changes
> * Environmental changes
> 
> 
> **Globalization and its impact on migration:**
> 
> * Increased mobility and accessibility of information and transportation
> * Growing interconnectedness of economies and societies
> * Spread of ideas and values
> * Increased awareness of different cultures and perspectives
"""

# https://oer.galileo.usg.edu/geo-textbooks/2/
original_url = ('https://oer.galileo.usg.edu/cgi/viewcontent.cgi?'
                'article=1002&context=geo-textbooks')

import argparse
import urllib.request 
import PyPDF2
import badinka as bd

config = bd.Config(
    vector_store_path = 'examples/data/geography.chroma'
)

def fetch():
  urllib.request.urlretrieve(original_url, 'examples/data/geography.pdf')

def extract():
  reader = PyPDF2.PdfReader('examples/data/geography.pdf')
  lines = []
  def _visit(text, cm, tm, font, size, lines=lines):
    if font and font['/BaseFont'] == '/PFELHC+Georgia' and tm[0] == 11.0:
      lines.append(text)
  for page in reader.pages[9:]:
    page.extract_text(visitor_text=_visit)
  f = open('examples/data/geography.txt', 'w')
  f.write(''.join(lines).replace('\n', ' '))
  f.close()


def embed():
  conductor = bd.Conductor(config)
  f = open('examples/data/geography.txt')
  raw = f.read()
  sentences = raw.split('. ')
  for i, s in enumerate(sentences):
    chunk = [s]
    for j in range(3):
      try:
        chunk.append(sentences[i+j])
      except IndexError:
        pass
    print(f'{i+1} of {len(sentences)}')
    if t := ''.join(chunk).strip():
      conductor.docs.append(bd.Document(content=t))


def query(q):
  conductor = bd.Conductor(config)
  reply = conductor.generate(
    bd.Instruction(
        role = 'a teacher',
        detail = 'in as much detail as you can',
        prompt = bd.Prompt(q),
        inject = bd.Injection(),
    ),
    options = bd.Options(
        output_tokens = 1024,
    ),
  )
  print(reply.content)


def topiclist():
  conductor = bd.Conductor(config)
  #conductor.config._log.config.immediate = True
  print(len(conductor.docs))
  p = bd.Prompt(
      'describe in one word or phrase what this text is about "{{context}}"'
  )
  for doc in conductor.docs.all():
    resp = conductor.generate(p, context=doc.content)
    print(resp.content)



def chat():
  while True:
    q = input('? ').strip()
    query(q)
  

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      'action',
      nargs='?',
      choices=['fetch', 'extract', 'embed', 'chat', 'query'],
      default='query')
  args = parser.parse_args()
  actions = {
      'fetch': fetch,
      'extract': extract,
      'embed': embed,
      'chat': chat,
      'query': lambda: query('why do people migrate'),
  }
  actions[args.action]()


if __name__ == '__main__':
  #main()
  topiclist()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
