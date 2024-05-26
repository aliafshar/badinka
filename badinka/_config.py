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
  generation_model_name: str = 'gemma'
  embeddings_model_name: str = 'mxbai-embed-large'
  embeddings_url: str = 'http://localhost:11434/api/embeddings'
  generation_url: str = 'http://localhost:11434/api/generate'
  vector_store_path: str = ':memory:'
  log: loguru._Logger = loguru.logger


# vim: ft=python sw=2 ts=2 sts=2 tw=120
