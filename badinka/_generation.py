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
import datetime

import jinja2
import ollama

from loguru import logger as log

from ._config import Config


@dataclass
class Options:
  """The options for a generation call."""

  #: The number of output tokens
  output_tokens: int = None

  def as_dict(self) -> dict[str, any]:
    """Generates the correct keywords for calling Ollama."""
    return {
        'num_predict': self.output_tokens,
    }

  def load_defaults(self, config) -> None: 
    """Load the default values from the overall configuration.

    Since most parameters have defaults in the configuration but are overridable
    per individual call, we provide a mechanism to update the unset options from
    their defaults.
    """
    if not self.output_tokens:
      self.output_tokens = config.generation_output_tokens


@dataclass
class Prompt:
  """A prompt with substitutable variables.

  BaDinka prompts use the complete [Jinja2]() templating language."""

  #: The template content as a string.
  template: str

  def render(self, **prompt_params: dict[str, any]) -> str:
    """Render the template with the given prompt parameters."""
    t = jinja2.Template(self.template)
    return t.render(**prompt_params)


@dataclass
class Injection:
  """Context injection parameters to populate the prompt context."""

  #: The number of results to populate the context.
  n_results: int = 10


@dataclass
class Instruction:
  """The instruction to generate for an LLM

  This is a high-level construct which contains a bunch of different parts to
  build a prompt for an LLM:

  1. The prompt is the prompt that will generate the final query for the LLM.
     This is a jinja2 template which can be substituted with parameters during
     the render.

  2. The context. You can populate this manually, or you can use the injection
     to automatically generate it from the document store based on the query.

  3. The role describes how you want the LLM to behave. This can be a person,
     such as "teacher" or describe the behavioural attributes of the LLM.

  4. Injection defines how the context will be populated from the document store
     with the query parameters. 

  """

  #: The prompt that provides the last part of the instruction.
  prompt: Prompt

  #: The parameters that control whether context is injected.
  inject: Injection = None

  #: The behavioural role that the generation will take.
  role: str = None

  #: The tone that the generation should take.
  tone: str = None

  #: The detail at which to generate
  detail: str = None

  #: The prompt context. If provided, the LLM will be given the context and
  #: instructed to use it to generate its response.
  #: Note: when an injection is provided this is overriden.
  context: str = None

  #: The hard-coded text query. If the prompt is provided this will be overriden
  #: with the rendered prompt.
  query: str = None

  #: The template for the complete instruction. This prompt has a default which
  #: can be overriden here.
  template: Prompt = field(
      default_factory=lambda: Prompt(
        template=default_instruction_template)
  )

  def render_query(self, **kw) -> str:
    """Renders the query part of the prompt."""
    return self.prompt.render(**kw)

  def render(self, **kw) -> str:
    """Renders the complete prompt."""
    q = self.render_query(**kw)
    p = self.template.render(
        role = self.role,
        tone = self.tone,
        detail = self.detail,
        context = self.context,
        query = q,
    )
    return p


@dataclass
class Reply:
  """Generated text from the LLM."""

  #: The text content of the reply.
  content: str

  #: The model that was used for generation.
  model_name: str

  #: The date and time of the response.
  date: datetime.datetime

  #: The duration that the entire generation took.
  duration: int

  #: The duration of evaluation.
  eval_duration: int

  #: The duration of loading the model.
  load_duration: int

  #: The duration of the actual prompt.
  prompt_duration: int

  @classmethod
  def from_response(cls, resp):
    """Create this instance from the Ollama response."""
    return cls(
        content=resp['response'],
        date=datetime.datetime.fromisoformat(resp['created_at']),
        model_name=resp['model'],
        duration=resp['total_duration'],
        eval_duration=resp['eval_duration'],
        load_duration=resp['load_duration'],
        prompt_duration=resp['prompt_eval_duration'],
    )


class Generator:
  """Generator calls LLMs and generates text."""

  def __init__(self, config: Config):
    self.config = config

  def generate_from_text(self, text: str,
      options: Options = None) -> Reply:
    """Generate a response from simple text."""
    if not options:
      options = Options()
    resp = ollama.generate(
        model=self.config.generation_model_name,
        prompt=text,
        options=options.as_dict(),
    )
    reply = Reply.from_response(resp)
    return reply

  def generate_from_prompt(self, prompt: Prompt,
      options: Options=None,
      **prompt_params) -> Reply:
    """Generate a response from a prompt with parameters."""
    t = prompt.render(**prompt_params)
    return self.generate_from_text(text=t, options=options)

  def generate_from_instruction(self, instruction: Instruction,
      options: Options=None,
      **prompt_params) -> Reply:
    """Generate a response from a complete instruction."""
    t = instruction.render(**prompt_params)
    print(t)
    return self.generate_from_text(text=t, options=options)


#: The default template for an instruction.
default_instruction_template = """
{%- if role %}
You should behave as {{role}}.
{%- endif %}
{%- if tone %}
You should adopt a tone that is {{tone}}.
{%- endif %}
{%- if context %}
Using only the following context, answer the question below
{%- if detail %} {{ detail }}{%- endif %}:

Context: {{context}}
{%- endif %}
{%- if check %}
Check your work and don't answer if you don't know.
{%- endif %}

{{query}}
"""

# vim: ft=python sw=2 ts=2 sts=2 tw=80
