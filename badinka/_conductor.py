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


from dataclasses import dataclass, field

from ._base import Configurable
from ._config import Config
from ._documents import Document, DocumentStore, Query
from ._generation import Generator, Prompt, Reply, Instruction, Options, Chain
  

class Conductor(Configurable):
  """Conductor is the thing you need to run the orchestra."""

  def configure(self):
    self.docs: DocumentStore = DocumentStore(self.config)
    self.generator: Generator = Generator(self.config)

  def generate(self,
      generator_input: str | Prompt | Instruction,
      options: Options=None,
      **prompt_params: dict[str, any]):
    #log.debug(f'input={generator_input} options={options}', action='generate')
    match generator_input:
      case str():
        return self.generator.generate_from_text(
            generator_input,
            options=options)
      case Prompt():
        return self.generator.generate_from_prompt(
            generator_input,
            options=options, **prompt_params)
      case Instruction():
        if generator_input.inject:
          q = generator_input.render_query(**prompt_params)
          docs = self.docs.query(
              Query(
                  text=q,
                  n_results=generator_input.inject.n_results,
              ),
          )
          generator_input.context = '\n'.join(d.content for d in docs)
        return self.generator.generate_from_instruction(
            generator_input,
            options=options, **prompt_params)
      case Chain():
        return self.generator.generate_from_chain(generator_input,
            options=options, **prompt_params)


# vim: ft=python sw=2 ts=2 sts=2 tw=80
