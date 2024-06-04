

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


