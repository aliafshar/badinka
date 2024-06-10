# BaDinka

**Minimalist AI orchestration library for local LLMs**

Skip this, go straight to the [API Docs](https://badinka-website.web.app/).

## What is a minimalist orchestration framework?

BaDinka provides the following:

1. Model generation with Gemma (or other Ollama models)
2. Document storage with Chromadb

and simplifies the connection between them in order to prompt the LLM with
instructions.

## Installation

The dependencies are:

1. Jinja2 (for templating)
2. Ollama client library (for talking to Ollama)
3. Chroma db client library (for talking to Chroma)

So, in whatever virtualenv setup you have:

```shell
pip install jinja2 ollama chromadb
```

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

## Configuration

You can configure the default models and parameters for generation etc in the
Config class.

```python
@dataclass
class Config:
  """Configuration for all BaDinka activity."""

  #: The default Ollama model used for text generation.
  generation_model_name: str = 'gemma'

  #: The default number of output tokens for generation.
  generation_output_tokens: int = 64

  #: The default Ollama model used for generating embeddings.
  embeddings_model_name: str = 'mxbai-embed-large'

  #: The Ollama URL used for embeddings.
  embeddings_url: str = 'http://localhost:11434/api/embeddings'

  #: The Ollama URL used for generation.
  generation_url: str = 'http://localhost:11434/api/generate'

  #: The default vector store path. When using `:memory:` an in-memory-only
  #: store is used with no persistence. When a path is given, that path is used
  #: as a persistent store.
  vector_store_path: str = ':memory:'

  #: Whether logging calls should be immediately dumped to stdout
  log_immediate: bool = False

  #: Whether logging should dump the entire log at exit
  log_dump_at_exit: bool = False

  #: Configuration for logging
  log_config: LogConfig = field(init=False)
```

Additionally, you can set per-generation options passed explicitly to every
generate call.

```python
@dataclass
class Options:
  """The options for a generation call."""

  #: The number of output tokens
  tokens: int = None

  #: The output format (only "json" is acceptable)
  json: bool = False

```


# Examples

(these are automatically imported from the [examples/](examples/) directory of
the source code)


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

## LLM generation with instruction
View/Download source: [gen1.py](examples/gen1.py)
### Rendered prompt

> You should behave as a poet.
> 
> why is the sky blue?

### Output (e.g.)

> In fields of clouds, where whispers meet,
> The sun's embrace, a gentle heat.
> Through scattered threads, a cosmic dance,
> Ray meets molecule, chance meets chance.
> 
> Blue, the hue that fills the frame,
> A symphony of scattered name.
> Rayleigh's dance, a wondrous sight,
> Explains the sky's ethereal light.
### Code
```python
import badinka as bd

def main():
  c = bd.Conductor()
  reply = c.generate(
      bd.Instruction(
        role='a poet',
        query='why is the sky blue?',
      ),
  )
  print(reply.content)

if __name__ == '__main__':
  main()
```

## LLM generation with prompt substitution
View/Download source: [gen2.py](examples/gen2.py)
### Rendered prompt

> Decsribe the effect of interest rates on house prices.

### Output (e.g.)

> **Interest rates have a significant impact on house prices:**
> 
> **1. Rising Interest Rates:**
> 
> * Increased borrowing costs reduce affordability.
> * Reduced demand can lead to lower house prices.
> * Investors may reduce investment in the housing market due to higher
>   borrowing costs.
> 
> 
> **2. Falling Interest Rates:**
> 
> * Lower borrowing costs increase affordability, making homeownership more
>   attainable.
> * Increased demand can drive up house prices.
> * Investors may become more active in the housing market due to lower
>   borrowing costs.
### Code
```python
import badinka as bd

def main():
  c = bd.Conductor()
  p = bd.Prompt('describe the effect of {{cause}} on {{effect}}')
  reply = c.generate(p, cause='interest rates', effect='house prices')
  print(reply.content)

if __name__ == '__main__':
  main()
```

## LLM generation with options
View/Download source: [gen3.py](examples/gen3.py)
### Rendered prompt

> why is the sky blue?

### Output (e.g.)

> **The sky is
### Code
```python
import badinka as bd

def main():
  c = bd.Conductor()
  reply = c.generate(
      'why is the sky blue?',
      bd.Options(tokens=4),
  )
  print(reply.content)

if __name__ == '__main__':
  main()
```

## LLM generation with JSON output
View/Download source: [gen4.py](examples/gen4.py)
### Rendered prompt

> Name some things in the sky, and their color, in JSON

### Output (e.g.)

```json
{
  "sky_elements": [
    {
      "name": "Sun",
      "color": "#FFD700"
    },
    {
      "name": "Moon",
      "color": "#FFFFFF"
    }
  ]
}
```
### Code
```python
import badinka as bd

def main():
  c = bd.Conductor()
  reply = c.generate(
      'Name some things in the sky, and their colour, in JSON',
      options=bd.Options(
        json=True,
        tokens=1024,
      ),
  )
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

## Retrieval augmented generation from a text book
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
  main()
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



