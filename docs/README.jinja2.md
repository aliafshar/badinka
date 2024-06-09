{#- This is the template that generates the README -#}

# BaDinka

**{{ subtitle }}**

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
{{ config }}
```

Additionally, you can set per-generation options passed explicitly to every
generate call.

```python
{{ options }}
```


# Examples

(these are automatically imported from the [examples/](examples/) directory of
the source code)

{% for example in examples %}
## {{ example.summary }}
View/Download source: [{{example.filename}}]({{ example.path }})
{{ example.description }}
### Code
```python
{{ example.source }}
```
{% endfor %}

{{ motivation }}



