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


"""Configuration settings for BaDinka.
"""

from dataclasses import dataclass, field

from ._logging import Log, LogConfig


@dataclass
class Config:
  """Configuration for all BaDinka activity."""

  #: The default Ollama model used for text generation.
  generation_model: str = 'gemma'

  #: The default number of output tokens for generation.
  generation_tokens: int = 64

  #: The default generation temperature
  generation_temperature: float = 0.7

  #: The default generation top_k
  generation_topk: int = 40

  #: The default generation top_p
  generation_topp: float = 0.9

  #: The Ollama URL used for generation.
  generation_url: str = 'http://localhost:11434/api/generate'

  #: The default Ollama model used for generating embeddings.
  embeddings_model: str = 'mxbai-embed-large'

  #: The Ollama URL used for embeddings.
  embeddings_url: str = 'http://localhost:11434/api/embeddings'

  #: The default vector store path. When using `:memory:` an in-memory-only
  #: store is used with no persistence. When a path is given, that path is used
  #: as a persistent store.
  vector_store_path: str = ':memory:'

  #: Whether logging calls should be immediately dumped to stdout
  log_immediate: bool = False

  #: Whether logging should dump the entire log at exit
  log_dump_at_exit: bool = False

  def __post_init__(self):
    self.log = Log(
        LogConfig(
          immediate = self.log_immediate,
          dump_at_exit = self.log_dump_at_exit,
        ),
    )

# vim: ft=python sw=2 ts=2 sts=2 tw=80
