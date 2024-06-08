# BaDinka

**Minimalist AI orchestration library for local LLMs**

Skip this, go straight to the [API Docs](https://badinka-website.web.app/).



## What is a minimalist orchestration framework?

BaDinka provides the following:

1. Model generation with Gemma (or other Ollama models)
2. Document storage with Chromadb

and simplifies the connection between them in order to prompt the LLM with
instructions.

## Underlying infrastructure

### Generation and embedding models

BaDinka uses [Ollama](), and defaults to use the [Gemma 7B]() model for
generation and the [mxbai-embed-large]() moddel for embeddings. You'll
need to install Ollama and have it running. The models will be pulled
first time they are used, but it's probably more sensible to pull them
separately.

```bash
ollama pull gemma
```

### Document storage

BaDinka uses [ChromaDB]() for storing and retrieving documents. This can
be with or without persistence. To use in-memory only pass the path
`:memory:` which will prevent any persistence.

```python
badinka.Config(
  vector_store_path = ':memory:'
)
```

# Configuration

You can configure the default models and parameters for generation etc in the
Config class, which can then be overriden for individual calls using Options
as needed.

{{ config }}




# Examples


## Basic LLM generation
View/Download source: [gen0.py](examples/gen0.py)
### Rendered prompt

> why is the sky blue?

### Output (e.g.)

> **The sky is blue due to a process called Rayleigh scattering.**
### Code
```python
import badinka as bd

def main():
  c = bd.Conductor()
  reply = c.generate('why is the sky blue?')
  print(reply.content)

if __name__ == '__main__':
  main()
```

## Basic retrieval augmented generation.
View/Download source: [rag0.py](examples/rag0.py)
### Rendered prompt

> You should behave as a gullible person.
> Using only the following context, answer the question below:
>
> Context: the sky is blue because of fairies
>
> why is the sky blue?

### Output (e.g.)

> Because of fairies, of course! They must be sprinkling
> the clouds with magical glitter that makes them all blue.
### Code
```python
import badinka as bd

def main():
  c = bd.Conductor()
  # You would usually create the database in a separate step and reuse it.
  # Here we create it on the fly.
  c.docs.append(
      bd.Document(content='the sky is blue because of fairies'),
  )
  reply = c.generate(
    bd.Instruction(
      role = 'a gullible person', # The AI is too smart otherwise.
      prompt = bd.Prompt('why is the sky blue?'),
      # Performs a document search and inserts the results into the context.
      inject = bd.Injection(),
    ),
    options = bd.Options(
      output_tokens=32,
    ),
  )
  print(reply.content)

if __name__ == '__main__':
  main()
```

## Geography tutor
View/Download source: [rag1.py](examples/rag1.py)
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
### Code
```python
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
```


# Motivation

(obligatory stream of consciousness)

Most orchestration frameworks are built to integrate every possible combination
of models, databases, etc. possible and are very good at making it possible to
swap components out. BaDinka is not that framework.

BaDinka doesn't particularly focus on the concept or arbitrary pipelines either.
I found, while using Langchain and Haystack (two excellent frameworks you should
probably check out if you are using Python) that things became overly complex,
but overly un-granular, and in an effort to support *everything*, that *nothing*
was particularly well supported. This is not a criticism, but a common effect of
generalization in software development - the lowest common denominator effect.



