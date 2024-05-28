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


"""Configuration settings for BaDinka."""


import dataclasses

import loguru


@dataclasses.dataclass
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

  #: The logging mechanism.
  log: loguru._Logger = loguru.logger


# vim: ft=python sw=2 ts=2 sts=2 tw=80
