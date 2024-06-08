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




# Configuration

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
<meta name="generator" content="pdoc 0.10.0" />
<title>badinka._config API documentation</title>
<meta name="description" content="Configuration settings for BaDinka." />
<link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/sanitize.min.css" integrity="sha256-PK9q560IAAa6WVRRh76LtCaI8pjTJ2z11v0miyNNjrs=" crossorigin>
<link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/typography.min.css" integrity="sha256-7l/o7C8jubJiy74VsKTidCy1yBkRtiUGbVkYBylBqUg=" crossorigin>
<link rel="stylesheet preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/styles/github.min.css" crossorigin>
<style>:root{--highlight-color:#fe9}.flex{display:flex !important}body{line-height:1.5em}#content{padding:20px}#sidebar{padding:30px;overflow:hidden}#sidebar > *:last-child{margin-bottom:2cm}.http-server-breadcrumbs{font-size:130%;margin:0 0 15px 0}#footer{font-size:.75em;padding:5px 30px;border-top:1px solid #ddd;text-align:right}#footer p{margin:0 0 0 1em;display:inline-block}#footer p:last-child{margin-right:30px}h1,h2,h3,h4,h5{font-weight:300}h1{font-size:2.5em;line-height:1.1em}h2{font-size:1.75em;margin:1em 0 .50em 0}h3{font-size:1.4em;margin:25px 0 10px 0}h4{margin:0;font-size:105%}h1:target,h2:target,h3:target,h4:target,h5:target,h6:target{background:var(--highlight-color);padding:.2em 0}a{color:#058;text-decoration:none;transition:color .3s ease-in-out}a:hover{color:#e82}.title code{font-weight:bold}h2[id^="header-"]{margin-top:2em}.ident{color:#900}pre code{background:#f8f8f8;font-size:.8em;line-height:1.4em}code{background:#f2f2f1;padding:1px 4px;overflow-wrap:break-word}h1 code{background:transparent}pre{background:#f8f8f8;border:0;border-top:1px solid #ccc;border-bottom:1px solid #ccc;margin:1em 0;padding:1ex}#http-server-module-list{display:flex;flex-flow:column}#http-server-module-list div{display:flex}#http-server-module-list dt{min-width:10%}#http-server-module-list p{margin-top:0}.toc ul,#index{list-style-type:none;margin:0;padding:0}#index code{background:transparent}#index h3{border-bottom:1px solid #ddd}#index ul{padding:0}#index h4{margin-top:.6em;font-weight:bold}@media (min-width:200ex){#index .two-column{column-count:2}}@media (min-width:300ex){#index .two-column{column-count:3}}dl{margin-bottom:2em}dl dl:last-child{margin-bottom:4em}dd{margin:0 0 1em 3em}#header-classes + dl > dd{margin-bottom:3em}dd dd{margin-left:2em}dd p{margin:10px 0}.name{background:#eee;font-weight:bold;font-size:.85em;padding:5px 10px;display:inline-block;min-width:40%}.name:hover{background:#e0e0e0}dt:target .name{background:var(--highlight-color)}.name > span:first-child{white-space:nowrap}.name.class > span:nth-child(2){margin-left:.4em}.inherited{color:#999;border-left:5px solid #eee;padding-left:1em}.inheritance em{font-style:normal;font-weight:bold}.desc h2{font-weight:400;font-size:1.25em}.desc h3{font-size:1em}.desc dt code{background:inherit}.source summary,.git-link-div{color:#666;text-align:right;font-weight:400;font-size:.8em;text-transform:uppercase}.source summary > *{white-space:nowrap;cursor:pointer}.git-link{color:inherit;margin-left:1em}.source pre{max-height:500px;overflow:auto;margin:0}.source pre code{font-size:12px;overflow:visible}.hlist{list-style:none}.hlist li{display:inline}.hlist li:after{content:',\2002'}.hlist li:last-child:after{content:none}.hlist .hlist{display:inline;padding-left:1em}img{max-width:100%}td{padding:0 .5em}.admonition{padding:.1em .5em;margin-bottom:1em}.admonition-title{font-weight:bold}.admonition.note,.admonition.info,.admonition.important{background:#aef}.admonition.todo,.admonition.versionadded,.admonition.tip,.admonition.hint{background:#dfd}.admonition.warning,.admonition.versionchanged,.admonition.deprecated{background:#fd4}.admonition.error,.admonition.danger,.admonition.caution{background:lightpink}</style>
<style media="screen and (min-width: 700px)">@media screen and (min-width:700px){#sidebar{width:30%;height:100vh;overflow:auto;position:sticky;top:0}#content{width:70%;max-width:100ch;padding:3em 4em;border-left:1px solid #ddd}pre code{font-size:1em}.item .name{font-size:1em}main{display:flex;flex-direction:row-reverse;justify-content:flex-end}.toc ul ul,#index ul{padding-left:1.5em}.toc > ul > li{margin-top:.5em}}</style>
<style media="print">@media print{#sidebar h1{page-break-before:always}.source{display:none}}@media print{*{background:transparent !important;color:#000 !important;box-shadow:none !important;text-shadow:none !important}a[href]:after{content:" (" attr(href) ")";font-size:90%}a[href][title]:after{content:none}abbr[title]:after{content:" (" attr(title) ")"}.ir a:after,a[href^="javascript:"]:after,a[href^="#"]:after{content:""}pre,blockquote{border:1px solid #999;page-break-inside:avoid}thead{display:table-header-group}tr,img{page-break-inside:avoid}img{max-width:100% !important}@page{margin:0.5cm}p,h2,h3{orphans:3;widows:3}h1,h2,h3,h4,h5,h6{page-break-after:avoid}}</style>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js" integrity="sha256-Uv3H6lx7dJmRfRvH8TH6kJD1TSK1aFcwgx+mdg3epi8=" crossorigin></script>
<script>window.addEventListener('DOMContentLoaded', () => hljs.initHighlighting())</script>
</head>
<body>
<main>
<article id="content">
<header>
<h1 class="title">Module <code>badinka._config</code></h1>
</header>
<section id="section-intro">
<p>Configuration settings for BaDinka.</p>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python"># Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the &#34;License&#34;);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an &#34;AS IS&#34; BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


&#34;&#34;&#34;Configuration settings for BaDinka.&#34;&#34;&#34;

from dataclasses import dataclass, field

from ._logging import Log, LogConfig


@dataclass
class Config:
  &#34;&#34;&#34;Configuration for all BaDinka activity.&#34;&#34;&#34;

  #: The default Ollama model used for text generation.
  generation_model_name: str = &#39;gemma&#39;

  #: The default number of output tokens for generation.
  generation_output_tokens: int = 64

  #: The default Ollama model used for generating embeddings.
  embeddings_model_name: str = &#39;mxbai-embed-large&#39;

  #: The Ollama URL used for embeddings.
  embeddings_url: str = &#39;http://localhost:11434/api/embeddings&#39;

  #: The Ollama URL used for generation.
  generation_url: str = &#39;http://localhost:11434/api/generate&#39;

  #: The default vector store path. When using `:memory:` an in-memory-only
  #: store is used with no persistence. When a path is given, that path is used
  #: as a persistent store.
  vector_store_path: str = &#39;:memory:&#39;

  #: Configuration for logging
  log_config: LogConfig = field(default_factory=LogConfig)

  _log: Log = None

  @property
  def log(self):
    if not self._log:
      self._log = Log(self.log_config)
    return self._log



# vim: ft=python sw=2 ts=2 sts=2 tw=80</code></pre>
</details>
</section>
<section>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-classes">Classes</h2>
<dl>
<dt id="badinka._config.Config"><code class="flex name class">
<span>class <span class="ident">Config</span></span>
<span>(</span><span>generation_model_name: str = 'gemma', generation_output_tokens: int = 64, embeddings_model_name: str = 'mxbai-embed-large', embeddings_url: str = 'http://localhost:11434/api/embeddings', generation_url: str = 'http://localhost:11434/api/generate', vector_store_path: str = ':memory:', log_config: badinka._logging.LogConfig = &lt;factory&gt;)</span>
</code></dt>
<dd>
<div class="desc"><p>Configuration for all BaDinka activity.</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">@dataclass
class Config:
  &#34;&#34;&#34;Configuration for all BaDinka activity.&#34;&#34;&#34;

  #: The default Ollama model used for text generation.
  generation_model_name: str = &#39;gemma&#39;

  #: The default number of output tokens for generation.
  generation_output_tokens: int = 64

  #: The default Ollama model used for generating embeddings.
  embeddings_model_name: str = &#39;mxbai-embed-large&#39;

  #: The Ollama URL used for embeddings.
  embeddings_url: str = &#39;http://localhost:11434/api/embeddings&#39;

  #: The Ollama URL used for generation.
  generation_url: str = &#39;http://localhost:11434/api/generate&#39;

  #: The default vector store path. When using `:memory:` an in-memory-only
  #: store is used with no persistence. When a path is given, that path is used
  #: as a persistent store.
  vector_store_path: str = &#39;:memory:&#39;

  #: Configuration for logging
  log_config: LogConfig = field(default_factory=LogConfig)

  _log: Log = None

  @property
  def log(self):
    if not self._log:
      self._log = Log(self.log_config)
    return self._log</code></pre>
</details>
<h3>Class variables</h3>
<dl>
<dt id="badinka._config.Config.embeddings_model_name"><code class="name">var <span class="ident">embeddings_model_name</span> : str</code></dt>
<dd>
<div class="desc"><p>The default Ollama model used for generating embeddings.</p></div>
</dd>
<dt id="badinka._config.Config.embeddings_url"><code class="name">var <span class="ident">embeddings_url</span> : str</code></dt>
<dd>
<div class="desc"><p>The Ollama URL used for embeddings.</p></div>
</dd>
<dt id="badinka._config.Config.generation_model_name"><code class="name">var <span class="ident">generation_model_name</span> : str</code></dt>
<dd>
<div class="desc"><p>The default Ollama model used for text generation.</p></div>
</dd>
<dt id="badinka._config.Config.generation_output_tokens"><code class="name">var <span class="ident">generation_output_tokens</span> : int</code></dt>
<dd>
<div class="desc"><p>The default number of output tokens for generation.</p></div>
</dd>
<dt id="badinka._config.Config.generation_url"><code class="name">var <span class="ident">generation_url</span> : str</code></dt>
<dd>
<div class="desc"><p>The Ollama URL used for generation.</p></div>
</dd>
<dt id="badinka._config.Config.log_config"><code class="name">var <span class="ident">log_config</span> : badinka._logging.LogConfig</code></dt>
<dd>
<div class="desc"><p>Configuration for logging</p></div>
</dd>
<dt id="badinka._config.Config.vector_store_path"><code class="name">var <span class="ident">vector_store_path</span> : str</code></dt>
<dd>
<div class="desc"><p>The default vector store path. When using <code>:memory:</code> an in-memory-only
store is used with no persistence. When a path is given, that path is used
as a persistent store.</p></div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="badinka._config.Config.log"><code class="name">var <span class="ident">log</span></code></dt>
<dd>
<div class="desc"></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">@property
def log(self):
  if not self._log:
    self._log = Log(self.log_config)
  return self._log</code></pre>
</details>
</dd>
</dl>
</dd>
</dl>
</section>
</article>
<nav id="sidebar">
<h1>Index</h1>
<div class="toc">
<ul></ul>
</div>
<ul id="index">
<li><h3><a href="#header-classes">Classes</a></h3>
<ul>
<li>
<h4><code><a title="badinka._config.Config" href="#badinka._config.Config">Config</a></code></h4>
<ul class="">
<li><code><a title="badinka._config.Config.embeddings_model_name" href="#badinka._config.Config.embeddings_model_name">embeddings_model_name</a></code></li>
<li><code><a title="badinka._config.Config.embeddings_url" href="#badinka._config.Config.embeddings_url">embeddings_url</a></code></li>
<li><code><a title="badinka._config.Config.generation_model_name" href="#badinka._config.Config.generation_model_name">generation_model_name</a></code></li>
<li><code><a title="badinka._config.Config.generation_output_tokens" href="#badinka._config.Config.generation_output_tokens">generation_output_tokens</a></code></li>
<li><code><a title="badinka._config.Config.generation_url" href="#badinka._config.Config.generation_url">generation_url</a></code></li>
<li><code><a title="badinka._config.Config.log" href="#badinka._config.Config.log">log</a></code></li>
<li><code><a title="badinka._config.Config.log_config" href="#badinka._config.Config.log_config">log_config</a></code></li>
<li><code><a title="badinka._config.Config.vector_store_path" href="#badinka._config.Config.vector_store_path">vector_store_path</a></code></li>
</ul>
</li>
</ul>
</li>
</ul>
</nav>
</main>
<footer id="footer">
<p>Generated by <a href="https://pdoc3.github.io/pdoc" title="pdoc: Python API documentation generator"><cite>pdoc</cite> 0.10.0</a>.</p>
</footer>
</body>
</html>

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



